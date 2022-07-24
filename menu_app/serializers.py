from .models import Dish, Menu
from rest_framework import serializers


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            "name",
            "description",
            "price",
            "time_to_prepare",
            "is_vegan",
            "photo",
        )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("name", "description", "creation_date", "last_modified_date")


class MenuDetailSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        exclude = ("id",)


class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class CreateDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"
