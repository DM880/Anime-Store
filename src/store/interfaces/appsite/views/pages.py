from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views import generic as generic_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from collections import defaultdict


import os
import json
import random
import math
import stripe
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


from store.data.user.models import CustomUser as User, AccountDetail
from store.data.item.models import Item, ItemImage, ItemReview
from store.data.cart.models import Cart, EntryCart, HistoryOrder, HistoryEntryCart


from store.domain.user import validation
from store.domain.cart import queries as cart_queries, checkout
from store.domain.item import queries as item_queries


from .utils import rating_avg, pagination, get_session_key


class LandingPage(generic_views.TemplateView):
    template_name = "landing_page.html"


def error_404(request, exception):
    return render(request, "error_404.html", status=404)


# User


def sign_in(request):

    if request.user.is_authenticated:
        return redirect("main_store")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("main_store")
        else:
            return render(request, "user/sign_in.html", {"error": True})
    else:
        return render(request, "user/sign_in.html")


def sign_up(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        valid = validation.sign_up_validation(username, email, password1, password2)

        if valid == True:

            data_user = {
                "first_name": request.POST.get("fname"),
                "last_name": request.POST.get("lname"),
                "username": request.POST.get("username"),
                "date_of_birth": request.POST.get("birth"),
                "email": request.POST.get("email"),
                "password": request.POST.get("password1"),
            }

            User.objects.create_user(**data_user)

            return redirect("login")
        else:
            return render(request, "user/sign_up.html", {"valid": valid})

    return render(request, "user/sign_up.html")


@login_required
def sign_out(request):
    logout(request)
    return redirect("main_store")


def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": request.META["HTTP_HOST"],
                        "site_name": "Anime Slash",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    message = Mail(
                        from_email=settings.EMAIL_HOST,
                        to_emails=user.email,
                        subject=subject,
                        html_content=email,
                    )

                    try:
                        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                        response = sg.send(message)
                        print(response)
                        print(response.status_code)
                    except Exception as e:
                        print(e)

                    messages.success(
                        request,
                        "A message with reset password instructions has been sent to your inbox.",
                    )
                    return redirect("main_store")
            messages.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(
        request,
        "password_reset/password_reset.html",
        {"password_reset_form": password_reset_form},
    )


# Account


@login_required
def user_details(request):
    user = User.objects.get(email=request.user.email)
    try:
        shipping_details = AccountDetail.objects.get(user=user)
    except AccountDetail.DoesNotExist:
        shipping_details = None
    return render(
        request,
        "account/user_details.html",
        {"user": user, "shipping_details": shipping_details},
    )


@login_required
def my_orders(request):

    user = User.objects.get(email=request.user.email)
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = None

    completed_orders = HistoryOrder.objects.filter(cart=cart)
    all_items = Item.objects.all()

    history_entries = []
    tot_completed_orders = completed_orders.count()

    for order in completed_orders:
        history_entries += HistoryEntryCart.objects.filter(
            cart=cart, history_cart=order
        )

    context = {
        "completed_orders": completed_orders,
        "history_entries": history_entries,
    }

    return render(request, "account/my_orders.html", context)


@login_required
def my_reviews(request):

    user = User.objects.get(email=request.user.email)
    reviews = ItemReview.objects.filter(username=user)

    if request.method == "POST":
        review = request.POST.get("review")
        change = request.POST.get("change")
        pass

    return render(request, "account/my_reviews.html", {'reviews':reviews})


@login_required
def edit_account(request):

    user = User.objects.get(email=request.user.email)

    if request.method == "POST":

        update_user = User.objects.update_or_create()
        pass

    return render(request, "account/edit_account.html", {"user": user})


@login_required
def delete_account(request):

    return render(request, "account/delete_account.html")


# Store


def main_store(request):
    obj_items = Item.objects.all()
    page = request.GET.get("page", 1)
    page_range = 4

    all_items = pagination(page, obj_items, page_range)

    # get last page number
    tot_pages = int(math.ceil(obj_items.count() / page_range))

    return render(
        request,
        "store/main_store.html",
        {"all_items": all_items, "tot_pages": tot_pages},
    )


def item_page(request, item_id):
    item = Item.objects.get(id=item_id)
    reviews = ItemReview.objects.filter(item=item_id)
    all_images = ItemImage.objects.filter(item=item_id)
    all_items = Item.objects.all()
    tot_items_count = Item.objects.all().count()

    avg_rating_data = rating_avg(reviews)
    current_item_index = (*all_items,).index(item)
    reviews_count = reviews.count()
    more_reviews = False

    reccomendations = []
    shown_reviews = []
    previous_n = [
        current_item_index,
    ]

    if tot_items_count > 5:
        for x in range(5):
            n = random.randint(0, tot_items_count - 1)

            # exclude current item and previous n
            while n in previous_n:
                n = random.randint(0, tot_items_count - 1)

            reccomendations.append(all_items[n])
            previous_n.append(n)

    if reviews_count >= 5:
        more_reviews = True
        shown_reviews = [reviews[y] for y in range(5)]
    else:
        shown_reviews = [i for i in reviews]

    images = [image for i, image in enumerate(all_images) if i != 0]

    context = {
        "item": item,
        "reviews": shown_reviews,
        "more_reviews": more_reviews,
        "avg_rating_data": avg_rating_data,
        "reccomendations": reccomendations,
        "images": images,
    }

    return render(request, "store/item_page.html", context)


def search_item(request):
    items_category = request.GET.get("items_category")
    searched_item = request.GET.get("search-item")
    sorting_element = request.GET.get("sorting_by")

    if sorting_element is None:
        sorting_element = "price"

    obj_items = item_queries.search_and_sort(
        items_category, searched_item, sorting_element
    )

    page = request.GET.get("page", 1)
    page_range = 4

    tot_pages = int(math.ceil(obj_items.count() / page_range))

    all_items = pagination(page, obj_items, page_range)

    context = {
        "all_items": all_items,
        "searched_item": searched_item,
        "items_category": items_category,
        "tot_pages": tot_pages,
    }

    return render(request, "store/search_page.html", context)


def post_review(request, item_id):

    if request.method == "POST":
        data = {
            "username": User.objects.get(email=request.user.email),
            "item": Item.objects.get(id=item_id),
            "title": request.POST.get("title-rev-input"),
            "review": request.POST.get("txt-rev-description"),
            "rating": request.POST.get("rating"),
        }

        ItemReview.objects.create(**data)

        return redirect(reverse("item_page", args=(item_id,)))


class AllReviews(generic_views.TemplateView):
    template_name = "store/all_reviews.html"

    def get_context_data(self, **kwargs):
        context = super(AllReviews, self).get_context_data(**kwargs)
        item = self.kwargs["item_id"]
        context["reviews"] = ItemReview.objects.filter(item=item)
        return context


# Cart


def add_item_cart(request, item_id):
    quantity = request.POST.get("quantity")
    user = request.user

    # For guest users
    session_key = get_session_key(request)

    if quantity is None:
        quantity = 1
    else:
        quantity = int(quantity)

    cart_queries.add_item(user, item_id, quantity, session_key)

    data = {"valid": True, "quantity": quantity}

    return JsonResponse(data, status=200)


def remove_item_cart(request, item_id):
    quantity = request.POST.get("quantity")
    user = request.user

    session_key = get_session_key(request)

    if quantity is None:
        quantity = 1
    else:
        quantity = int(quantity)

    cart_queries.remove_item(user, item_id, quantity, session_key)

    # redirect to same page,if not found redirect to 'main_store'
    return redirect(request.META.get("HTTP_REFERER", "main_store"))


# Checkout


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

    context = {"cart": cart, "items": items, "subtotal": subtotal, "total": total}

    return render(request, "checkout/checkout_page.html", context)


def checkout_remove_entry(request, entry):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(user=user)
    else:
        cart = Cart.objects.get(session_key=request.session.session_key)

    checkout.remove_entry(entry, cart)

    data = {
        "valid": True,
        "url": reverse("checkout_page"),
    }

    return JsonResponse(data, status=200)


def checkout_update_quantity(request, entry):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(user=user)
    else:
        cart = Cart.objects.get(session_key=request.session.session_key)

    quantity = int(request.POST.get("quantity"))

    checkout.update_quantity(entry, quantity, cart)

    return redirect(request.META.get("HTTP_REFERER", "main_store"))


# Stripe Checkout


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):

    if request.method == "GET":
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            if request.user.is_authenticated:
                user = User.objects.get(email=request.user.email)
                user_detail = AccountDetail.objects.get(user=user)
                cart = Cart.objects.get(user=user)
                email = user.email
            else:
                cart = Cart.objects.get(session_key=request.session.session_key)
                email = None

            payment_session_key = request.session.session_key
            subtotal = int(round(cart.tot_price, 2) * 100)

            # ?session_id={CHECKOUT_SESSION_ID} redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url
                + "payment/success/"
                + payment_session_key
                + "/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "payment/cancelled/",
                customer_email=email,
                payment_method_types=["card"],
                mode="payment",
                shipping_address_collection={
                    "allowed_countries": ["US", "CA"],
                },
                shipping_options=[
                    {
                        "shipping_rate_data": {
                            "type": "fixed_amount",
                            "fixed_amount": {
                                "amount": 499,
                                "currency": "usd",
                            },
                            "display_name": "Shipping",
                        }
                    },
                ],
                line_items=[
                    {
                        "name": "Cart",
                        "quantity": 1,
                        "currency": "usd",
                        "amount": f"{subtotal}",
                    }
                ],
            )

            context = checkout_session.id
            return JsonResponse({"sessionId": context})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":

        print("Payment was successful.")

    return HttpResponse(status=200)


def payment_successful(request, payment_session_key):

    if payment_session_key == request.session.session_key:
        if request.user.is_authenticated:
            user = User.objects.get(email=request.user.email)
            cart = Cart.objects.get(user=user)
            cart.purchased = True
            cart.save()
            checkout.clean_cart(cart)
        else:
            cart = Cart.objects.get(session_key=request.session.session_key)
            cart.delete()

    return render(request, "checkout/payment_successful.html")


class PaymentCancelled(generic_views.TemplateView):
    template_name = "checkout/payment_cancelled.html"
