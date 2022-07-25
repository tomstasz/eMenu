import django_filters
from django.core.mail import EmailMessage
from django.db import models as django_models
from django.db.models import Count
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dish, Menu
from .serializers import (CreateDishSerializer, CreateMenuSerializer,
                          DishSerializer, MenuDetailSerializer, MenuSerializer)


class MenuList(generics.ListAPIView):
    """View of all menus with at least one dish."""

    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "creation_date", "last_modified_date"]

    def get_queryset(self):
        queryset = Menu.objects.exclude(dishes__isnull=True)
        if "nazwa" in self.request.query_params:
            queryset = Menu.objects.exclude(dishes__isnull=True).order_by("name")
        if "dania" in self.request.query_params:
            queryset = (
                Menu.objects.exclude(dishes__isnull=True)
                .annotate(dishes_num=Count("dishes"))
                .order_by("-dishes_num")
            )
        return queryset


class MenuDetail(APIView):
    """Detailed view of single menu"""

    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, id):
        menu = self.get_object(id)
        serializer = MenuDetailSerializer(menu, context={"request": request})
        return Response(serializer.data)


class DishCreate(viewsets.ModelViewSet):
    """Endpoint to add new dish."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class MenuCreate(viewsets.ModelViewSet):
    """Endpoint to add new menu."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = CreateMenuSerializer


class MenuManage(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint to modify or delete menus."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateMenuSerializer
    queryset = Menu.objects.all()


class DishManage(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint to modify or delete dishes."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateDishSerializer
    queryset = Dish.objects.all()
