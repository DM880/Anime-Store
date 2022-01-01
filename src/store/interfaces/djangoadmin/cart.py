from django.contrib import admin


from store.data.cart.models import Cart, EntryCart


class EntryCartInLine(admin.TabularInline):
    model = EntryCart


class CartAdmin(admin.ModelAdmin):

    inlines = [EntryCartInLine]


admin.site.register(Cart, CartAdmin)
