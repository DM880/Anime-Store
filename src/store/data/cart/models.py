from django.db import models


from store.data.item.models import Item
from store.data.user.models import CustomUser as User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tot_count = models.IntegerField(default=0)
    tot_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    updated = models.DateTimeField(auto_now=True)
    purchase = models.BooleanField(default=False)

    def __str__(self):
        return f"user={self.user.username}/price={self.tot_price}/id={self.user_id}"


class EntryCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
