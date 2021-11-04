from store.data.item.models import Item
from store.data.cart.models import Cart, EntryCart


def update_cart(cart, item, quantity, command):
    if command == "add":
        cart.tot_count += 1
        cart.tot_price += item.price * quantity
        cart.save()
    else:
        cart.tot_count -= 1
        cart.tot_price += item.price * quantity
        cart.save()


def add_item_user(request, item_id):

    carts = Cart.objects.all()
    item = Item.objects.get(item_id=item_id)

    for cart in carts:
        if cart.user == request.user:
            EntryCart.objects.create(cart=cart, item=item)
            update_cart(cart, item, quantity=1, command="add")
            return

    cart_user=Cart.objects.create(user=request.user)
    EntryCart.objects.create(cart=cart_user, item=item)
    update_cart(cart, item, quantity=1, command="add")


def add_item_guest(request, item_id):

    item = Item.objects.get(item_id=item_id)
    EntryCart.objects.create(item=item)


def remove_item(request, item_id):

    cart = Cart.objects.get(user=request.user)
    item = Item.objects.get(item_id=item_id)
    entries = EntryCart.objects.filter(cart=cart, item=item)
    quantity_item = EntryCart.objects.filter(item=item).count()
    quantity = 1

    if quantity > quantity_item:
        for entry in entries:
            entry.delete()

    for entry in entries:
        if quantity == 0:
            update_cart(cart, item, quantity, command="")
            return
        entry.delete()
        quantity -= 1

    update_cart(cart, item, quantity_item, command="")
