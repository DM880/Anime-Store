from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import pages


urlpatterns = [
    path('', pages.LandingPage.as_view(), name="landing_page"),
    path('checkout/', pages.checkout, name="checkout"),

    #User
    path('signup/', pages.sign_up, name="sign_up"),
    path('login/', pages.sign_in, name="login"),

    #Store
    path('store/', pages.main_store, name="main_store"),
    path('store/<item_id>/', pages.item_page, name="item_page"),

    #Cart
    path('cart/add/<item_id>/', pages.add_item_cart, name="add_item"),
    path('cart/remove/<item_id>/', pages.remove_item_cart, name="remove_item"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)