from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import pages

urlpatterns = [
    path('', pages.landing_page, name="landing_page"),
    path('user/', pages.user_creation, name="user_creation"),
    path('store/', pages.main_store, name="main_store"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)