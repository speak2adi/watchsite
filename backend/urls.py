from django.urls import path
from .views import (ProductListView, AddNewProduct, AddToCart, CartView, PaystackPayment)
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('search/', ProductListView.as_view(), name='products-search'),
    path('filter/', ProductListView.as_view(), name='products-filter'),
    path('add-product/', AddNewProduct.as_view(), name='add-product'),
    path('add-cart/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/pay/', PaystackPayment.as_view(), name='pay-payment'),

]
