from django.shortcuts import render, redirect
from django.views import generic as generic_views
from django.http import JsonResponse
import json


from store.data.user.models import CustomUser as User
from store.data.item.models import Item
from store.data.cart.models import Cart


from store.domain.user import validation
from store.domain.cart import queries


class LandingPage(generic_views.TemplateView):
    template_name = "landing_page.html"


#User

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('main_store')

    if request.method == "POST":
        if validation.sign_in_validation(request):
            return redirect('main_store')
        else:
            return render(request, "user/sign_in.html", {'error':True})
    else:
        return render(request, "user/sign_in.html")


def sign_up(request):

    if request.method == "POST":

        if validation.sign_up_validation(request):
            return redirect('login')
        else:
            return redirect('landing_page')

    return render(request, "user/sign_up.html")


#Store

def main_store(request):
    all_items = Item.objects.all()

    return render(request, "store/main_store.html", {'all_items':all_items})


#Cart

def add_item_cart(request, item):
    if request.user.is_authenticated:
        queries.add_item_user(request, item)
    else:
        queries.add_item_guest(request, item)
    return redirect('main_store')
