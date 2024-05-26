import uuid
from django.db import models
from common.db import BaseModel
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser,BaseModel):
    user_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    post_number = models.CharField(verbose_name='post_number', null=True, blank=True, max_length=10)
    state = models.CharField(verbose_name='state', null=False, blank=True, max_length=100)
    suburb = models.CharField(verbose_name='suburb', null=True, blank=True, max_length=100)
    address1 = models.CharField(verbose_name='address1', null=False, blank=False, max_length=150)
    address2 = models.CharField(verbose_name='address2', null=True, blank=True, max_length=150)
    recipient_name = models.CharField(verbose_name='recipient_name', null=False, blank=False, max_length=150)
    abn = models.CharField(verbose_name='abn', null=True, blank=True, max_length=150)
    acn = models.CharField(verbose_name='acn', null=True, blank=True, max_length=150)
    company_name = models.CharField(verbose_name='company_name', null=False, blank=False, max_length=150)
    industry = models.CharField(verbose_name='industry', null=True, blank=True, max_length=100)
    position = models.CharField(verbose_name='position', null=True, blank=True, max_length=50)
    first_name = None
    last_name = None

    class Meta:
        db_table = 'users'
        verbose_name = 'users'

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='blacklisted_tokens', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token