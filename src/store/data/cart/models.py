from django.db import models


from store.data.item.models import Item
from store.data.user.models import CustomUser as User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40)
    tot_count = models.IntegerField(default=0)
    tot_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    updated = models.DateTimeField(auto_now=True)
    purchased = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "user",
            "session_key",
        )

    def __str__(self):
        return f"user={self.user}/price={self.tot_price}/id={self.user_id}"


class EntryCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.item.price * self.quantity


class HistoryOrder(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    items = models.CharField(max_length=50)
    tot_count = models.IntegerField(default=0)
    tot_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    purchased = models.DateTimeField(auto_now=True)
