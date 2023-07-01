from django.db import models
from PIL import Image
from django.contrib.auth.models import User


# Product models
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='products')
    stock = models.IntegerField()
    orders = models.ManyToManyField("Order", through='OrderProduct')

    def __str__(self):
        return self.name


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Order models
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    order_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
                                    default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" Order by {self.customer.username}"

    # function used to determine the total cost of the items/products in the orderlist
    def total_cost(self):
        total_cost = 0
        # the orderproduct_set is an attribute created by Django when you use a many-to-many relationship through
        # an intermediary model.
        for order_product in self.orderproduct_set.all():
            total_cost += order_product.product.price * order_product.quantity
        return total_cost

    def add_product(self, product, quantity):
        # adding an item to the cart
        try:
            order_product = OrderProduct.objects.get(order=self, product=product)
            order_product.quantity += quantity
        except OrderProduct.DoesNotExist:
            order_product = OrderProduct.objects.create(order=self, product=product, quantity=quantity)
            order_product.save()

    def remove_product(self, product):
        # removing an item from the cart
        try:
            order_product = OrderProduct.objects.get(order=self, product=product)
            order_product.delete()
        except OrderProduct.DoesNotExist:
            pass

    def update_product(self, product, quantity):
        # Update the quantity of the product in the cart
        try:
            order_product = OrderProduct.objects.get(order=self, product=product)
            order_product.quantity = quantity
            if product.stock < quantity:
                raise ValueError("Stock is less than required quantity")
        except OrderProduct.DoesNotExist:
            raise ValueError("This product is not in the cart")


# Item ordered
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product}"

