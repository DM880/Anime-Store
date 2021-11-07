from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime


from store.data.item.models import Item
from store.data.user.models import CustomUser as User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tot_count = models.IntegerField(default=0)
    tot_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} have {} items for {} $".format(self.user.username, self.tot_count, self.tot_price)


class EntryCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "item:{} {}".format(self.quantity, self.item.item_name)
