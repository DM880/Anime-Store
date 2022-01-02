from store.data.user.models import CustomUser as User
from store.data.item.models import Item
from store.data.cart.models import Cart, EntryCart, HistoryOrder


def update_cart(cart, item, quantity):

    cart.tot_count += quantity
    cart.tot_price += item.price * quantity
    cart.save()


def add_item(user, item_id, quantity, session_key):

    item = Item.objects.get(id=item_id)

    cart = get_cart(user, session_key)

    EntryCart.objects.create(cart=cart, item=item, quantity=quantity)

    update_cart(cart, item, quantity)


def remove_item(user, item_id, quantity, session_key):

    cart = get_cart(user, session_key)

    item = Item.objects.get(id=item_id)
    entries = EntryCart.objects.filter(cart=cart, item=item)
    quantity_item = EntryCart.objects.filter(cart=cart, item=item).count()

    if quantity_item == 0:
        return

    elif quantity >= quantity_item:
        for entry in entries:
            entry.delete()
        quantity = quantity_item * -1
        update_cart(cart, item, quantity)
        return

    else:
        temp_quantity = quantity
        for entry in entries:
            if temp_quantity == 0:
                quantity *= -1
                update_cart(cart, item, quantity)
                return
            entry.delete()
            temp_quantity -= 1


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


def get_cart(user, session_key):
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
    else:
        cart = Cart.objects.get_or_create(session_key=session_key)[0]

    return cart
