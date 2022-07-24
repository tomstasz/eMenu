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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.conf import settings
from menu_app import views


router = routers.DefaultRouter()
router.register(r"dish", views.DishCreate, basename="dish")
router.register(r"menu", views.MenuCreate, basename="menu")

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include(router.urls)),
        path("index/", views.MenuList.as_view(), name="menu-list"),
        path("index/<int:id>", views.MenuDetail.as_view(), name="menu-detail"),
        path("menu/<int:pk>", views.MenuManage.as_view(), name="menu-manage"),
        path("dish/<int:pk>", views.DishManage.as_view(), name="dish-manage"),
    ]
    + staticfiles_urlpatterns()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
