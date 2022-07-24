from .models import Dish, Menu
from .serializers import (
    DishSerializer,
    MenuSerializer,
    MenuDetailSerializer,
    CreateMenuSerializer,
    CreateDishSerializer,
)
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.db import models as django_models
from rest_framework.views import APIView
from django.http import Http404


class MenuList(generics.ListAPIView):
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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class MenuCreate(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = CreateMenuSerializer


class MenuManage(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateMenuSerializer
    queryset = Menu.objects.all()


class DishManage(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateDishSerializer
    queryset = Dish.objects.all()
