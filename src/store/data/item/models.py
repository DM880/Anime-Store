from django.db import models


from store.data.category.models import CategoryItem as Category


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reviews = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="other")

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    item_image = models.ImageField(upload_to="item/")