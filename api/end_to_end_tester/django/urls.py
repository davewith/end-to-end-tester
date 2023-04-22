from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from rest_framework.routers import DefaultRouter, SimpleRouter
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from end_to_end_tester.apps.people.views import MeViewSet

admin.site.site_title = _("End To End Tester")
admin.site.site_header = _("End To End Tester")


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("me", MeViewSet, basename="me")

urlpatterns = [
    path("back/admin/", admin.site.urls),
    path("back/api/", include(router.urls)),
    path("cms/", include(wagtailadmin_urls)),
    path("back/documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns = [
        path(
            "back/api/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),
        path(
            "back/api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "back/api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ] + urlpatterns
