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
    # installa black per la sintassi
    # l'id e' generato automaticamente perche' lo crei?
    item_id = models.AutoField(primary_key=True)

    # siamo gia' nell'item, perche' usi il prefix?
    item_name = models.CharField(max_length=200)
    item_description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTH)

    def __str__(self):
        # questo e' piu' leggibile
        # return f"{self.name}, {self.category}"
        return "{}/{}".format(self.item_name, self.category)

    def first_image(self):
        # crash se non esiste l'immagine
        # usa self.image.first()
        return self.image.all()[0]


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='image')
    # siamo gia' nell'item, perche' usi il prefix?
    # image basta
    item_image = models.ImageField(upload_to="item/",)


class ItemReview(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, ) # related_name="reviews" ?
    # title
    title_review = models.CharField(max_length=20, blank=True)
    review = models.TextField(max_length=500, blank=True)
    # creation and update? timestamp e' il valore registrato il name field dovrebbe dare un significato
    timestamp = models.DateTimeField(blank=True, null=True,default=datetime.datetime.now)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title_review