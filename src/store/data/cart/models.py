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
        return "{} have {} items, total price {}".format(self.user, self.tot_count, self.tot_price)


class EntryCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)


@receiver(post_save, sender=EntryCart)
def update_cart(sender, instance, **kwargs):
    tot_item_cost = instance.quantity * instance.item.price
    instance.cart.tot_price += tot_item_cost
    instance.cart.tot_count += instance.quantity
    instance.cart.updated = datetime.now()