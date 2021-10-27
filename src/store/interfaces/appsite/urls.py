from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import pages

urlpatterns = [
    path('', pages.LandingPage.as_view(), name="landing_page"),

    #User
    path('user/', pages.user_creation, name="user_creation"),

    #Store
    path('store/', pages.main_store, name="main_store"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)