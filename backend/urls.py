from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.sites.site.index_title = "EMS"
admin.site.site_header = "EMS"
admin.sites.site.site_title = "EMS"


urlpatterns = [
    path("", include("account.urls")),
    path("system/", include("frontend.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
