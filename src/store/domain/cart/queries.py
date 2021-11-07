from store.data.user.models import CustomUser as User
from store.data.item.models import Item
from store.data.cart.models import Cart, EntryCart

"""
Queries sono in sola lettura qui vedo parecche "operations"
"""


# definisci i tipi
# se c'e' un problema dovresti fare un revert altrimenti ti ritrovi il db corrotto
def update_cart(cart, item, quantity, command):
    if command:  # cosa significa command?
        cart.tot_count += quantity
        cart.tot_price += item.price * quantity
        cart.save()
    else:
        cart.tot_count -= quantity
        cart.tot_price -= item.price * quantity
        cart.save()


# non si passa la request al domain.
# qui stai crendo una relazione alla request di cui `add_item` conosce "is_autenthicated"
def add_item(request, item_id, quantity):

    item = Item.objects.get(item_id=item_id)

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart=Cart.objects.create(user=request.user)

        EntryCart.objects.create(cart=cart, item=item, quantity=quantity)
        update_cart(cart, item, quantity, command="add")

    else:
        cart = guest_cart()
        EntryCart.objects.create(cart=cart, item=item, quantity=quantity)
        update_cart(cart, item, quantity, command="add")


def remove_item(request, item_id, quantity):

    # user non e' identificato qui. Hai passato la request
    # la request e' MALE
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
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
        update_cart(cart, item, quantity, command="")  # questo command che mandi e' davvero strano
        return

    else:
        quantity_query = quantity  # strano anche questo perche' query mi viene in mente una queryset, ma quantity e' un int.
        for entry in entries:
            if quantity_query == 0:
                update_cart(cart, item, quantity, command="")
                return
            entry.delete()
            quantity_query -= 1


# hai un guest cart unico per tutti gli user?
def guest_cart():
    user = User.objects.get(username='guest')
    cart = Cart.objects.get(user=user)
    return cart