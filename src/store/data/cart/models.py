from django.db import models


from store.data.item.models import Item
from store.data.user.models import CustomUser as User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)