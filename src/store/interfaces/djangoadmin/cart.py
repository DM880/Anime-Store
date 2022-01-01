from django.contrib import admin


from store.data.cart.models import Cart, EntryCart, HistoryOrder


class EntryCartInLine(admin.TabularInline):
    model = EntryCart


class HistoryOrderInLine(admin.TabularInline):
    model = HistoryOrder


class CartAdmin(admin.ModelAdmin):

    inlines = [EntryCartInLine, HistoryOrderInLine]


admin.site.register(Cart, CartAdmin)
