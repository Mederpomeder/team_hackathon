from django.db import models

from account.models import CustomUser
from product.models import Product


class Order(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)





