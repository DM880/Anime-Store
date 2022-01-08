from django.contrib import admin


from store.data.cart.models import Cart, EntryCart, HistoryOrder, HistoryEntryCart


class EntryCartInLine(admin.TabularInline):
    model = EntryCart


class HistoryOrderInLine(admin.TabularInline):
    model = HistoryOrder


class HistoryEntryInLine(admin.TabularInline):
    model = HistoryEntryCart


class CartAdmin(admin.ModelAdmin):

    inlines = [EntryCartInLine, HistoryOrderInLine, HistoryEntryInLine]


admin.site.register(Cart, CartAdmin)
