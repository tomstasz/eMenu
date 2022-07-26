from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from menu_app.models import Dish, Menu


class DishTestCase(APITestCase):
    def setUp(self):
        self.dish = Dish.objects.create(
            name="test_dish",
            description="test description",
            price=12.00,
            time_to_prepare=6,
            is_vegan=True,
        )

    def test_dish_create(self):
        url = reverse("dish-list")
        data = {
            "name": "new_dish",
            "description": "new description",
            "price": 13.00,
            "time_to_prepare": 7,
            "is_vegan": False,
        }
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        response = self.client.post(url, data)
        created_dish = Dish.objects.get(name=response.data["name"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 2)
        self.assertEqual(data["name"], created_dish.name)
        self.assertEqual(data["description"], created_dish.description)
        self.assertEqual(data["price"], created_dish.price)
        self.assertEqual(data["time_to_prepare"], created_dish.time_to_prepare)
        self.assertEqual(data["is_vegan"], created_dish.is_vegan)

    def test_dish_create_return_403__when_user_not_authenticated(self):
        url = reverse("dish-list")
        data = {
            "name": "new_dish",
            "description": "new description",
            "price": 13.00,
            "time_to_prepare": 7,
            "is_vegan": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Dish.objects.filter(name=data["name"]).exists())

    def test_dish_update(self):
        url = reverse("dish-manage", kwargs={"pk": self.dish.pk})
        changed_data = {
            "name": "changed name",
            "description": "new description",
            "price": 13.00,
            "time_to_prepare": 7,
            "is_vegan": False,
        }

        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        response = self.client.put(url, changed_data)
        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], changed_data["name"])

    def test_dish_update_return_403__when_user_not_authenticated(self):
        url = reverse("dish-manage", kwargs={"pk": self.dish.pk})
        changed_data = {
            "name": "changed name",
            "description": "new description",
            "price": 13.00,
            "time_to_prepare": 7,
            "is_vegan": False,
        }

        response = self.client.put(url, changed_data)
        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(
            Dish.objects.get(id=self.dish.id).name, changed_data["name"]
        )

    def test_dish_delete(self):
        url = reverse("dish-manage", kwargs={"pk": self.dish.pk})
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())

    def test_dish_delete_return_403__when_user_not_authenticated(self):
        url = reverse("dish-manage", kwargs={"pk": self.dish.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Dish.objects.filter(id=self.dish.id).exists())

    def test_dish_model_returns_name(self):
        self.assertEqual(str(self.dish), self.dish.name)


class MenuTestCase(APITestCase):
    def setUp(self):
        self.dish_1 = Dish.objects.create(
            name="test_dish_1",
            description="test description_1",
            price=14.00,
            time_to_prepare=8,
            is_vegan=True,
        )
        self.dish_2 = Dish.objects.create(
            name="test_dish_2",
            description="test description_2",
            price=15.00,
            time_to_prepare=9,
            is_vegan=False,
        )
        self.dish_3 = Dish.objects.create(
            name="test_dish_3",
            description="test description_3",
            price=16.00,
            time_to_prepare=10,
            is_vegan=True,
        )
        self.menu = Menu.objects.create(
            name="test_menu",
            description="test menu description",
        )
        self.menu.dishes.add(self.dish_1)

    def test_menu_create(self):
        url = reverse("menu-list")
        data = {
            "name": "new_menu",
            "description": "new menu description",
            "dishes": [self.dish_2.id, self.dish_3.id],
        }
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        response = self.client.post(url, data)
        created_menu = Menu.objects.get(name=response.data["name"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(data["name"], created_menu.name)
        self.assertEqual(data["description"], created_menu.description)
        self.assertEqual(created_menu.dishes.count(), 2)

    def test_menu_create_return_403__when_user_not_authenticated(self):
        url = reverse("menu-list")
        data = {
            "name": "new_menu",
            "description": "new menu description",
            "dishes": [self.dish_2.id, self.dish_3.id],
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Menu.objects.filter(name=data["name"]).exists())

    def test_menu_list(self):
        url = reverse("menus-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Menu.objects.count())

    def test_menu_list__not_showing_menu_with_no_dishes(self):
        menu_2 = Menu.objects.create(
            name="test_menu_2",
            description="test menu 2 description",
        )

        url = reverse("menus-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Menu.objects.filter(id=menu_2.id).exists())
        self.assertEqual(len(response.data), Menu.objects.count() - 1)

    def test_menu_detail(self):
        url = reverse("menu-detail", kwargs={"id": self.menu.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.menu.name)
        self.assertEqual(response.data["description"], self.menu.description)
        self.assertEqual(response.data["dishes"][0]["name"], self.dish_1.name)

    def test_menu_update(self):
        url = reverse("menu-manage", kwargs={"pk": self.menu.pk})
        changed_data = {
            "name": "changed menu name",
            "description": "new description",
            "price": 13.00,
            "time_to_prepare": 7,
            "is_vegan": False,
            "dishes": [self.dish_2.id],
        }

        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        response = self.client.put(url, changed_data)
        self.menu.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], changed_data["name"])
        self.assertEqual(response.data["dishes"][0], self.dish_2.id)

    def test_menu_update_return_403__when_user_not_authenticated(self):
        url = reverse("menu-manage", kwargs={"pk": self.menu.pk})
        changed_data = {
            "name": "changed menu name",
            "description": "new description",
            "price": 13.00,
            "time_to_prepare": 7,
            "is_vegan": False,
            "dishes": [self.dish_2.id],
        }

        response = self.client.put(url, changed_data)
        self.menu.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(
            Menu.objects.get(id=self.menu.id).name, changed_data["name"]
        )
        self.assertNotEqual(
            Menu.objects.get(id=self.menu.id).dishes.first(), self.dish_2
        )

    def test_menu_delete(self):
        url = reverse("menu-manage", kwargs={"pk": self.menu.pk})
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=self.menu.id).exists())

    def test_menu_delete_return_403__when_user_not_authenticated(self):
        url = reverse("menu-manage", kwargs={"pk": self.menu.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Menu.objects.filter(id=self.menu.id).exists())

    def test_menu_model_returns_name(self):
        self.assertEqual(str(self.menu), self.menu.name)
