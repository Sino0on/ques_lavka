from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # path("__debug__/", include("debug_toolbar.urls")),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/product/", include("product.urls")),
    path('api/v1/admin/', admin.site.urls),
    path("api/v1/docs/", include("openapi.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)