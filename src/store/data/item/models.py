from django.db import models
import datetime


CATEGORY_CHOICES = (
    (ANI := "ANIME", "anime"),
    (MAN := "MANGA", "manga"),
    (ACT := "ACTION_FIGURE", "action_figure"),
    (COS := "COSPLAY", "cosplay"),
    (APP := "APPAREL", "apparel"),
    (GAM := "GAMING", "gaming"),
    (OTH := "OTHER", "other"),
    )


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTH)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_image = models.ImageField(upload_to="item/")


class ItemReview(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title_review = models.CharField(max_length=20, blank=True)
    review = models.TextField(max_length=500, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True,default=datetime.datetime.now)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title_review