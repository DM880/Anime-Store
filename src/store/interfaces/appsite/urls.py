from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import pages


urlpatterns = [

    path('', pages.LandingPage.as_view(), name="landing_page"),

    #User
    path('signup/', pages.sign_up, name="sign_up"),
    path('login/', pages.sign_in, name="login"),
    path('logout/', pages.sign_out, name="logout"),

    #Store
    path('store/', pages.main_store, name="main_store"),
    path('store/<item_id>/', pages.item_page, name="item_page"),
    path('store/<item_id>/post_review/', pages.post_review, name="post_review"),
    path('search/', pages.search_item, name="search_item"),

    #Cart
    path('cart/add/<item_id>/', pages.add_item_cart, name="add_item"),
    path('cart/remove/<item_id>/', pages.remove_item_cart, name="remove_item"),

    #Checkout
    path('checkout/', pages.checkout_page, name="checkout_page"),
    path('checkout/remove/<entry>/', pages.checkout_remove_entry, name="checkout_remove_entry"),
    path('checkout/update/<entry>/', pages.checkout_update_quantity, name="checkout_update_quantity"),

    #Stripe Checkout
    path('config/', pages.stripe_config , name="stripe_config"),
    path('create-checkout-session/', pages.create_checkout_session, name="create_checkout_session"),
    path('payment/success/', pages.PaymentSuccessful.as_view(), name="payment_successful"),
    path('payment/cancelled/', pages.PaymentCancelled.as_view(), name="payment_cancelled"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)