from django.contrib import admin

from store.data.item.models import Item, ItemImage, ItemReview
from store.data.category.models import CategoryItem as Category

class ItemImageInLine(admin.TabularInline):
    model = ItemImage


class ReviewInLine(admin.StackedInline):
    model = ItemReview


class ItemAdmin(admin.ModelAdmin):

    inlines = [
            ItemImageInLine,
            ReviewInLine,
        ]


admin.site.register(Item, ItemAdmin)