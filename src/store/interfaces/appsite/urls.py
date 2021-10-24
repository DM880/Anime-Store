from django.urls import path

from .views import pages

urlpatterns = [
    path('', pages.landing_page, name="landing_page"),
    path('user/', pages.user_creation, name="user_creation"),
]