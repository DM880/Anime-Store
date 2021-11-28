from store.data.user.models import CustomUser as User
from store.data.item.models import Item
from store.data.cart.models import Cart, EntryCart


def update_cart(cart, item, quantity):

    cart.tot_count += quantity
    cart.tot_price += item.price * quantity
    cart.save()


def remove_entry(entry,user):

    cart = Cart.objects.get(user=user)
    entry_cart = EntryCart.objects.get(cart=cart, id=entry)
    item = entry_cart.item
    quantity = entry_cart.quantity * -1

    entry_cart.delete()
    update_cart(cart, item, quantity)

    return


