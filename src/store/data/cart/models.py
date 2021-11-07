from django.db import models
# vari import non necessari qua sotto
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime


from store.data.item.models import Item
from store.data.user.models import CustomUser as User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tot_count = models.IntegerField(default=0)
    tot_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # anche qui, stesso problema dell'entry cart
        return "{} have {} items for ${}".format(self.user.username, self.tot_count, self.tot_price)
        # questo e' un poco meglio e non fa chiamate il db
        # return f"{self.id} price={self.tot_price} user={self.user_id}"


class EntryCart(models.Model):
    # questa soluzione potrebbe avere dei problemi se l'item cambia. Se ad esempio c'e' un acquisto nel cart e tutto e' ok
    # ma se in futuro l'item cambia, cambia anche l'entrycart di prodotti gia' acquistati... e' un dubbio che mi e' venuto
    # guardando il codice.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        # questo e' un problema. per stampare "se stesso" il cart la entry deve andare via card.user e username.
        # da evitare.
        return "{}/item:{} {}".format(self.cart.user.username, self.quantity, self.item.item_name)
