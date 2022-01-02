from store.data.user.models import CustomUser as User
from store.data.item.models import Item
from store.data.cart.models import Cart, EntryCart


def update_cart(cart, item, quantity):

    cart.tot_count += quantity
    cart.tot_price += item.price * quantity
    cart.save()


def remove_entry(entry, cart):
    entry_cart = EntryCart.objects.get(cart=cart, id=entry)
    item = entry_cart.item
    quantity = entry_cart.quantity * -1

    entry_cart.delete()
    update_cart(cart, item, quantity)

    return


def update_quantity(entry, quantity, cart):
    entry_cart = EntryCart.objects.get(cart=cart, id=entry)
    item = entry_cart.item
    quantity_remove = entry_cart.quantity * -1

    update_cart(cart, item, quantity_remove)

    entry_cart.quantity = quantity
    entry_cart.save()

    update_cart(cart, item, quantity)

    return


def clean_cart(cart):
    if cart.purchased:
        entries = EntryCart.objects.filter(cart=cart)
        HistoryOrder.objects.create(
            cart=cart,
            items=[entry.item.id for entry in entries],
            tot_count=cart.tot_count,
            tot_price=cart.tot_price,
            purchased=cart.updated,
        )
        cart.tot_count = 0
        cart.tot_price = 0
        cart.purchased = False
        cart.save()
        entries.delete()
