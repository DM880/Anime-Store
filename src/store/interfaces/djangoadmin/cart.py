from django.contrib import admin


from store.data.cart.models import Cart, EntryCart


admin.site.register(Cart)
admin.site.register(EntryCart)