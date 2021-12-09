from django.shortcuts import render, redirect, reverse
from django.views import generic as generic_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random

#For AJAX
from django.http import JsonResponse
import json


from store.data.user.models import CustomUser as User
from store.data.item.models import Item, ItemReview
from store.data.cart.models import Cart, EntryCart


from store.domain.user import validation
from store.domain.cart import queries, checkout


from .utils import rating_avg, search_and_sort, get_session_key


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


@login_required
def sign_out(request):
    logout(request)
    return redirect('main_store')


#Store

def main_store(request):
    all_items = Item.objects.all()

    return render(request, "store/main_store.html", {'all_items':all_items})


def item_page(request, item_id):
    item = Item.objects.get(id=item_id)
    reviews = ItemReview.objects.filter(item=item_id)
    avg_rating_data = rating_avg(reviews)
    all_items = Item.objects.all()
    tot_items_count = Item.objects.all().count()

    reccomendations = []

    for x in range(5):
        n = random.randint(0,tot_items_count-1)
        reccomendations.append(all_items[n])

    return render(request, 'store/item_page.html', {'item':item, 'reviews':reviews, 'avg_rating_data':avg_rating_data, 'reccomendations':reccomendations})


def search_item(request):
    searched_item = request.GET.get('search-item')
    sorting_element = request.GET.get('sorting_by')
    items_category = request.GET.get('items_category')

    if searched_item is None:
        searched_item = request.GET.get('search-val')
    if sorting_element is None:
        sorting_element = "price"

    items = search_and_sort(items_category, searched_item, sorting_element)

    return render(request, 'store/search_page.html', {'all_items':items, 'searched_item':searched_item, 'items_category':items_category})


#Cart

def add_item_cart(request, item_id):
    quantity = request.POST.get('quantity')
    user = request.user

    session_key = get_session_key(request)

    if quantity is None:
        quantity = 1
    else:
        quantity = int(quantity)

    queries.add_item(user, item_id, quantity, session_key)

    return JsonResponse({"valid":True,"quantity":quantity}, status = 200)


def remove_item_cart(request, item_id):
    quantity = request.POST.get('quantity')
    user = request.user

    session_key = get_session_key(request)

    if quantity is None:
        quantity = 1
    else:
        quantity = int(quantity)

    queries.remove_item(user, item_id, quantity, session_key)

    # redirect to same page,if not found redirect to 'main_store'
    return redirect(request.META.get('HTTP_REFERER', 'main_store'))


#Checkout

def checkout_page(request):

    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(user=user)
    else:
        session_key = get_session_key(request)
        cart = Cart.objects.get_or_create(session_key=session_key)[0]

    items = EntryCart.objects.filter(cart=cart)

    subtotal = cart.tot_price
    total = 4.99 + float(subtotal)

    return render(request, "checkout_page.html", {'cart':cart, 'items':items, 'subtotal':subtotal, 'total':total})


def checkout_remove_entry(request, entry):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(user=user)
    else:
        cart = Cart.objects.get(session_key=request.session.session_key)

    checkout.remove_entry(entry,cart)

    data = {
        'valid':True,
        'url':reverse('checkout_page'),
    }

    return JsonResponse(data, status = 200)


def checkout_update_quantity(request, entry):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(user=user)
    else:
        cart = Cart.objects.get(session_key=request.session.session_key)

    quantity = int(request.POST.get('quantity'))

    checkout.update_quantity(entry, quantity, cart)

    return redirect(request.META.get('HTTP_REFERER', 'main_store'))