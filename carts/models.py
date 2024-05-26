import uuid
from django.db import models
from common.db import BaseModel
from django.conf import settings
from productions.models import ProductionItem

# Create your models here.
class Cart(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        db_table = 'carts'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductionItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product')  # Enforces one CartItem per product in each cart

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"