from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True, blank=False)
    date_of_birth = models.DateField(auto_now=False, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(default=timezone.now)
    id = models.AutoField(primary_key=True)

    # Replace username with email for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ("created",)
        db_table = "store_user"


class AccountDetail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    created = models.DateField(auto_now_add=True)
