from django.test import TestCase
from django.conf import settings
from .models import *

settings.configure()

# Testing models
class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objrcts.create(
            name='My Test',
            description='My Test Product Description',
            price='10.045',
            stock='100',
        )

    def test_name(self):
        product = Product.objects.get(id=1)
        max_length = product.attr_meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_decimals(self):
        product = Product.objects.get(id=1)
        decimal_places = product.attr_meta.get('price').decimal_places
        self.assertEquals(decimal_places, 2)


