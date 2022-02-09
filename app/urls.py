from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import (
    DEFAULT_ROUTES,
    view_log
)

router = routers.DefaultRouter()

router = DefaultRouter()
for basename, viewset_cls in DEFAULT_ROUTES:
    if viewset_cls is not None:
        router.register(basename, viewset_cls, basename=basename)  # type: ignore


# for basename, viewset_cls in DEFAULT_ROUTES:
#     if viewset_cls is not None:
#         router.register(basename, viewset_cls, basename=basename)  # type: ignore

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "view-log/<int:log_id>/<str:view_token>", view_log, name="view_log"
    ),
]
