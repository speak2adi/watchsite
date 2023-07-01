from rest_framework.exceptions import NotFound
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (IsAuthenticated, IsAdminUser)
from .serializers import (ProductSerializer, OrderProductSerializer, OrderSerializer)
from .models import (Product, OrderProduct, Order)
from .filters import (ProductFilter)
from django_filters import rest_framework as filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.db import transaction
from .permissions import IsMerchant
import paystackapi
from paystackapi.transaction import Transaction


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name']



# add new product to database view
class AddNewProduct(LoginRequiredMixin, CreateAPIView):
    queryset = Product
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class EditProducts(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = Product
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AddToCart(LoginRequiredMixin, CreateAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        product_data = request.data.get('product')
        if not product_data:
            return Response({'detail': 'Product data is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_data['id'])
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        quantity = request.data.get('quantity', 1)
        if quantity < 1:
            return Response({'detail': 'Quantity must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)
        if product.stock < quantity:
            return Response({'detail': 'Insufficient stock.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create the cart Order object associated with the customer
        order = Order.objects.get_or_create(customer=request.user, status='cart')[0]
        # Create or retrieve the OrderProduct object associated with the Order and Product
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
        # If the OrderProduct already exists, update its quantity field by adding the new quantity
        # to the existing quantity
        if not created:
            order_product.quantity += quantity
            order_product.save()
        # Otherwise, set the quantity field to the new quantity value
        else:
            order_product.quantity = quantity
            order_product.save()
        # Serialize the Order object and return the serialized data with a 201 Created response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieving cart for current user .customer
        return Order.objects.filter(customer=self.request.user).prefetch_related('order_products__product')

    @transaction.atomic
    def perform_update(self, serializer):
        # Add or Update Cart Item
        product_data = self.request.data.get('product')
        try:
            product = Product.objects.get(id=product_data['id'])
        except Product.DoesNotExist:
            raise NotFound(detail='Product Not Found')
        quantity = self.request.data.get('quantity', 1)
        order = self.get_object().select_related('order_product')
        if quantity > 0:
            order.update_product(product, quantity)
        else:
            order.remove_product(product)

    @transaction.atomic
    def perform_destroy(self, instance):
        # Removing all Item from the Cart
        order_product = OrderProduct.objects.filter(order=instance).select_related('product')
        order_product.delete()

    def delete(self, request, *args, **kwargs):
        # Deleting an Item/Product from Cart
        order = self.get_object()
        product_data = self.request.data.get('product')
        product_id = product_data.get('id')
        order_product = get_object_or_404(order.order_products, order=order, product_id=product_id)
        order_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaystackPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the order
        order_id = kwargs.get('pk')
        order = Order.objects.get(id=order_id)
        total_amount = order.total_cost()

        paystackapi.secret_key = settings.PAY_STACK_SECRET_KEY

        transaction = Transaction.initialize(
            amount=total_amount * 100,
            email=order.customer.email,

        )
        return Response({'authorization_url': transaction.authorization_url})

    def get(self, request, *args, **kwargs):
        reference = request.query_parms('reference')
        paystackapi.secret_key = settings.PAY_STACK_SECRET_KEY

        transaction = Transaction.verify(reference)
        if transaction.status == 'success':
            order_id = kwargs.get('pk')
            order = Order.objects.get(id=order_id)
            order.order_status = 'Completed'
            return Response({'Message: Transaction Successful'})
        else:
            return Response({'Message: Transaction Unsuccessful'})
