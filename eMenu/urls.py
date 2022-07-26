"""eMenu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from menu_app import views

schema_view = get_schema_view(
    openapi.Info(
        title="eMenu API",
        default_version="v1",
        description="Endpointy dla menu z wieloma potrawami",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()
router.register(r"dish", views.DishCreate, basename="dish")
router.register(r"menu", views.MenuCreate, basename="menu")

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include(router.urls)),
        path("index/", views.MenuList.as_view(), name="menus-list"),
        path("index/<int:id>", views.MenuDetail.as_view(), name="menu-detail"),
        path("menu/<int:pk>", views.MenuManage.as_view(), name="menu-manage"),
        path("dish/<int:pk>", views.DishManage.as_view(), name="dish-manage"),
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
    + staticfiles_urlpatterns()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
