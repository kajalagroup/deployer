from django.urls import include, path
from rest_framework import routers
from .views import (
    TestView
)

router = routers.DefaultRouter()

# for basename, viewset_cls in DEFAULT_ROUTES:
#     if viewset_cls is not None:
#         router.register(basename, viewset_cls, basename=basename)  # type: ignore

urlpatterns = [
    path("", include(router.urls)),
    path("test/", TestView.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
