from store.data.user.models import CustomUser as User
from store.data.item.models import Item
from store.data.cart.models import Cart, EntryCart


def update_cart(cart, item, quantity, command):

    if command:
        cart.tot_count += quantity
        cart.tot_price += item.price * quantity
        cart.save()
    else:
        cart.tot_count -= quantity
        cart.tot_price -= item.price * quantity
        cart.save()


def add_item(user, item_id, quantity):

    item = Item.objects.get(item_id=item_id)

    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart=Cart.objects.create(user=user)

        EntryCart.objects.create(cart=cart, item=item, quantity=quantity)
        update_cart(cart, item, quantity, command="add")

    else:
        cart = guest_cart()
        EntryCart.objects.create(cart=cart, item=item, quantity=quantity)
        update_cart(cart, item, quantity, command="add")


def remove_item(user, item_id, quantity):

    if user.is_authenticated:
        cart = Cart.objects.get(user=user)
    else:
        cart = guest_cart()

    item = Item.objects.get(item_id=item_id)
    entries = EntryCart.objects.filter(cart=cart, item=item)
    quantity_item = EntryCart.objects.filter(cart=cart, item=item).count()

    if quantity_item == 0:
        return

    elif quantity > quantity_item or quantity == quantity_item:
        for entry in entries:
            entry.delete()
        quantity = quantity_item
        update_cart(cart, item, quantity, command="")
        return

    else:
        temp_quantity = quantity
        for entry in entries:
            if temp_quantity == 0:
                update_cart(cart, item, quantity, command="")
                return
            entry.delete()
            quantity_query -= 1


def guest_cart():
    user = User.objects.get(username='guest')
    cart = Cart.objects.get(user=user)
    return cart