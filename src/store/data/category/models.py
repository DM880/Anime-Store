from django.db import models


CATEGORY_CHOICES = (
    (ANI := "ANIME", "anime"),
    (MAN := "MANGA", "manga"),
    (ACT := "ACTION_FIGURE", "action_figure"),
    (COS := "COSPLAY", "cosplay"),
    (APP := "APPAREL", "apparel"),
    (GAM := "GAMING", "gaming"),
    )


class CategoryItem(models.Model):
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES)