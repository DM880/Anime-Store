from django.shortcuts import render, redirect, reverse
from django.views import generic as generic_views
from django.contrib.auth import authenticate, login
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

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('main_store')
        else:
            return render(request, "user/sign_in.html", {'error':True})
    else:
        return render(request, "user/sign_in.html")


def sign_up(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        valid = validation.sign_up_validation(username, email, password1, password2)

        if valid == True:

            data_user = {
                'first_name':request.POST.get('fname'),
                'last_name':request.POST.get('lname'),
                'username':request.POST.get('username'),
                'date_of_birth':request.POST.get('birth'),
                'email':request.POST.get('email'),
                'password':request.POST.get('password1'),
                }

            User.objects.create_user(**data_user)

            return redirect('login')
        else:
            return render(request, "user/sign_up.html", {'valid':valid})

    return render(request, "user/sign_up.html")


#Store

def main_store(request):
    all_items = Item.objects.all()
    return render(request, "store/main_store.html", {'all_items':all_items})


def item_page(request, item_id):
    item = Item.objects.get(item_id=item_id)
    return render(request, 'store/item_page.html', {'item':item})


#Cart

def add_item_cart(request, item_id):

    quantity = request.POST.get('quantity')
    user = request.user

    if quantity is None:
        quantity = 1

    else:
        quantity = int(quantity)

    queries.add_item(user, item_id, quantity)

    #redirect to same page,if not found redirect to 'main_store'
    return redirect(request.META.get('HTTP_REFERER', 'main_store'))


def remove_item_cart(request, item_id):

    quantity = request.POST.get('quantity')
    user = request.user

    if quantity is None:
        quantity = 1

    else:
        quantity = int(quantity)

    queries.remove_item(user, item_id, quantity)

    return redirect(request.META.get('HTTP_REFERER', 'main_store'))

