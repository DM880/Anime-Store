from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True, blank=False)
    date_of_birth = models.DateField(auto_now=False, null=True, blank=True)
    email = models.EmailField(max_length=200,unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    time_created = models.DateTimeField(default=timezone.now)
    user_id = models.AutoField(primary_key=True)

    #Replace username with email for authenticate function
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('time_created',)
        db_table = 'store_user'