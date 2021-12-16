from django.db import models
from django.db.models import Avg
import datetime


from store.data.user.models import CustomUser as User


CATEGORY_CHOICES = (
    (ANI := "ANIME", "anime"),
    (MAN := "MANGA", "manga"),
    (ACT := "ACTION_FIGURE", "action_figure"),
    (APP := "APPAREL", "apparel"),
    (GAM := "GAMING", "gaming"),
    (OTH := "OTHER", "other"),
    )


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTH)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}/{self.category}"

    def first_image(self):
        return self.image.first()

    def average_review(self):
        review = ItemReview.objects.filter(item=self.id).aggregate(average=Avg('rating'))
        count = ItemReview.objects.filter(item=self.id).count()
        avg=0
        if review["average"] is not None:
            avg=float(review["average"])
        data = {
            'avg':avg,
            'count':count,
        }
        return data


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to="item/",)


class ItemReview(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=20, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 5+1)], blank=True)
    posted = models.DateTimeField(blank=True, null=True,default=datetime.datetime.now)

    class Meta:
        ordering = ('-posted',)

    def __str__(self):
        return self.title