from .models import *
from rest_framework import serializers
from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        name = Category
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    # overriding the create method to allow creating an order object
    # with associated orderproduct objects
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
        return order

    # overriding the create method to allow creating an order object
    # with associated orderproduct objects
    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', None)
        instance.order_status = validated_data.get('order_status', instance.order_status)
        instance.save()
        if products_data:
            instance.products.all().delete()
            for product_data in products_data:
                OrderProduct.objects.create(order=instance, **product_data)
        return instance
