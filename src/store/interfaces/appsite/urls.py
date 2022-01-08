from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


from .views import pages


urlpatterns = [
    path("", pages.LandingPage.as_view(), name="landing_page"),
    # User
    path("signup/", pages.sign_up, name="sign_up"),
    path("login/", pages.sign_in, name="login"),
    path("logout/", pages.sign_out, name="logout"),
    # Password Reset
    path("password_reset/", pages.password_reset, name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Account
    path("account/user_details/", pages.user_details, name="user_details"),
    path("account/my_orders/", pages.my_orders, name="my_orders"),
    path("account/my_reviews/", pages.my_reviews, name="my_reviews"),
    path("account/edit_review/<item_id>/<review_id>", pages.edit_review, name="edit_review"),
    path("account/edit_account/", pages.edit_account, name="edit_account"),
    path("account/delete_account/", pages.delete_account, name="delete_account"),
    # Store
    path("store/", pages.main_store, name="main_store"),
    path("search/", pages.search_item, name="search_item"),
    path("store/<item_id>/", pages.item_page, name="item_page"),
    path("store/<item_id>/post_review/", pages.post_review, name="post_review"),
    path("store/reviews/<item_id>/", pages.AllReviews.as_view(), name="all_reviews"),
    # Cart
    path("cart/add/<item_id>/", pages.add_item_cart, name="add_item"),
    path("cart/remove/<item_id>/", pages.remove_item_cart, name="remove_item"),
    # Checkout
    path("checkout/", pages.checkout_page, name="checkout_page"),
    path(
        "checkout/remove/<entry>/",
        pages.checkout_remove_entry,
        name="checkout_remove_entry",
    ),
    path(
        "checkout/update/<entry>/",
        pages.checkout_update_quantity,
        name="checkout_update_quantity",
    ),
    # Stripe Checkout
    path("config/", pages.stripe_config, name="stripe_config"),
    path("webhook/", pages.stripe_webhook, name="stripe_webhook"),
    path(
        "create-checkout-session/",
        pages.create_checkout_session,
        name="create_checkout_session",
    ),
    path(
        "payment/success/<payment_session_key>/",
        pages.payment_successful,
        name="payment_successful",
    ),
    path(
        "payment/cancelled/", pages.PaymentCancelled.as_view(), name="payment_cancelled"
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
