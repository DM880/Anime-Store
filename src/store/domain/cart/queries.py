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


def add_item(request, item_id, quantity):

    carts = Cart.objects.all()
    item = Item.objects.get(item_id=item_id)

    if request.user.is_authenticated:
        for cart in carts:
            if cart.user == request.user:
                EntryCart.objects.create(cart=cart, item=item, quantity=quantity)
                update_cart(cart, item, quantity, command="add")
                return

        cart_user=Cart.objects.create(user=request.user)
        EntryCart.objects.create(cart=cart_user, item=item, quantity=quantity)
        update_cart(cart, item, quantity, command="add")

    else:
        EntryCart.objects.create(item=item, quantity=quantity)


def remove_item(request, item_id, quantity):

    cart = Cart.objects.get(user=request.user)
    item = Item.objects.get(item_id=item_id)
    entries = EntryCart.objects.filter(cart=cart, item=item)
    quantity_item = EntryCart.objects.filter(item=item).count()

    if quantity_item == 0:
        return

    elif quantity > quantity_item or quantity == quantity_item:
        for entry in entries:
            entry.delete()
            update_cart(cart, item, quantity, command="")
            return
    else:
        quantity_query = quantity
        for entry in entries:
            if quantity_query == 0:
                update_cart(cart, item, quantity, command="")
                return
            entry.delete()
            quantity_query -= 1
