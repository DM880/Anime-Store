from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import pages

urlpatterns = [
    path('', pages.LandingPage.as_view(), name="landing_page"),

    #User
    path('signup/', pages.signup, name="signup"),
    path('login/', pages.sign_in, name="login"),

    #Store
    path('store/', pages.main_store, name="main_store"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)