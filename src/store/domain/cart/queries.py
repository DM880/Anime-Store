from store.data.item import models
from store.data.cart import models


class Cart(object):


    def __init__(self):
        all_cart = []


    def add_item(self, item_id):

        cart = Cart.objects.all().filter(user=request.user)
        item = Item.objects.get(item_id=item_id)
        EntryCart.objects.create(cart=cart, item=item)


    def remove_item(self, item_id):

        cart = Cart.objects.all().filter(user=request.user)
        item = Item.objects.get(item_id=item_id)
        cart.remove(item)
