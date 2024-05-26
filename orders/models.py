import uuid
from django.db import models
from common.db import BaseModel
from django.conf import settings
from productions.models import ProductionItem
from django.db.models import Sum

class StatusChoices(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PAID = 2, 'Paid'
    CONFIRMED = 3, 'Confirmed'
    SHIPPED = 4, 'Shipped'
    Completed = 5, 'Completed'

# Create your models here.
class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', editable=False)
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_price = models.FloatField(default=0)
    mobile = models.CharField(max_length=20, null=False, blank=False)
    post_number = models.CharField(verbose_name='post_number', null=True, blank=True, max_length=10)
    state = models.CharField(verbose_name='state', null=False, blank=False, max_length=100)
    suburb = models.CharField(verbose_name='suburb', null=True, blank=True, max_length=100)
    address = models.CharField(verbose_name='address', null=False, blank=False, max_length=150)
    recipient_name = models.CharField(verbose_name='recipient_name', null=False, blank=False, max_length=150)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.PENDING, verbose_name='Status', null=False, blank=False)
    gst = models.FloatField(default=0)
    net_total_price = models.FloatField(default=0)
    delivery_method = models.CharField(verbose_name='delivery_method', null=True, blank=True, max_length=30)
    delivery_fee = models.FloatField(default=0)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductionItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    sum_price = models.FloatField(default=0)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def calculate_price(self):
        net_total_price = OrderItem.objects.filter(order=self.order).aggregate(total=Sum('sum_price'))['total'] or 0
        self.order.net_total_price = net_total_price
        self.order.total_price = net_total_price + self.order.gst + self.order.delivery_fee
        self.order.save(update_fields=['net_total_price', 'total_price'])

    def save(self, *args, **kwargs):
        self.sum_price = self.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
        self.calculate_price()

    def delete(self, *args, **kwargs):
        order = self.order
        super(OrderItem, self).delete(*args, **kwargs)
        order.refresh_from_db()
        self.calculate_price()