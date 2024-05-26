from django.db import models
from common.db import BaseModel

class StatusChoices(models.IntegerChoices):
    PUBLISHED = 1, 'Pulished'
    UNPUBLISHED = 2, 'UnPublished'
    OUTOFSTOCK = 3, 'OutOfStock'

# Create your models here.
class Production(BaseModel):
    name = models.CharField(verbose_name='name', null=False, blank=False, max_length=100)
    # description = models.TextField(verbose_name='description', null=False, blank=False)
    sku = models.CharField(verbose_name='sku', null=False, blank=False, max_length=7, unique=True)
    # class_grade = models.CharField(verbose_name='class_grade', null=False, blank=False, max_length=100)
    # standard = models.CharField(verbose_name='standard', null=False, blank=False, max_length=100)
    # plating = models.CharField(verbose_name='plating', null=False, blank=False, max_length=100)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.PUBLISHED, verbose_name='Status', null=False, blank=False)
    # single_item = models.BooleanField(verbose_name='single_item', default=True, blank=False)
    highest_price = models.FloatField(verbose_name='highest_price', null=True, blank=True, editable=False)
    lowest_price = models.FloatField(verbose_name='lowest_price', null=True, blank=True, editable=False)
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False)
    category = models.CharField(verbose_name='category', null=False, blank=False, max_length=50)
    specification = models.JSONField(verbose_name='specification', null=True, blank=True)
    images = models.JSONField(verbose_name='images', null=True, blank=True)

    class Meta:
        db_table = 'productions'
        verbose_name = 'productions'

    # def save(self, *args, **kwargs):
    #     super(Production, self).save(*args, **kwargs)
    #     if not self.sku:
    #         self.sku = self.generate_sku()
    #         self.save()

    # def generate_sku(self):
    #     return f"ee{self.id:06d}"

class ProductionItem(BaseModel):
    product = models.ForeignKey(Production, related_name='items', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='price', null=False, blank=False)
    promotion_price = models.FloatField(verbose_name='promotion_price', null=True, blank=True)
    sku = models.CharField(verbose_name='sku', null=False, blank=False, max_length=12, unique=True)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.UNPUBLISHED, verbose_name='Status', null=False, blank=False)
    specification = models.JSONField(verbose_name='specification', null=True, blank=True)

    class Meta:
        db_table = 'production_item'
        verbose_name = 'production_item'

    def save(self, *args, **kwargs):
        if self.promotion_price is None:
            self.promotion_price = self.price
        super(ProductionItem, self).save(*args, **kwargs)
        # if not self.sku:
        #     self.sku = self.generate_sku()
        #     self.save()
        self.update_production_prices()

    def update_production_prices(self):
        promotion_prices = self.product.items.values_list('promotion_price', flat=True)
        highest_price = max(promotion_prices)
        lowest_price = min(promotion_prices)
        production = self.product
        production.highest_price = highest_price
        production.lowest_price = lowest_price
        production.save()

    # def generate_sku(self):
    #     big_sku = self.product.sku
    #     number = self.product.items.count()
    #     return big_sku+f"{number:03d}"