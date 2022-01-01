from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static


from .appsite import urls as appsite_urls


handler404 = "store.interfaces.appsite.views.pages.error_404"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(appsite_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
