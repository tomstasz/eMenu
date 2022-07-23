from django.db import models


class Dish(models.Model):
    """Single dish avaliable in the menu"""
    name = models.CharField(max_length=128, verbose_name="Nazwa", db_index=True)
    description = models.TextField(verbose_name="Opis", null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena")
    time_to_prepare = models.IntegerField(verbose_name='Czas przygotowania ( w min.)', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")
    last_modified_date = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Data aktualizacji")
    is_vegan = models.BooleanField(default=False, verbose_name="Czy wegańskie?")
    photo = models.FileField(upload_to='media/')


    def __str__(self):
        return self.name


class Menu(models.Model):
    """Unique menu with dishes"""
    name = models.CharField(max_length=128, verbose_name="Nazwa", db_index=True, unique=True)
    description = models.TextField(verbose_name="Opis", blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")
    last_modified_date = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Data aktualizacji")
    dishes = models.ManyToManyField(Dish, verbose_name="Dania")

    def __str__(self):
        return self.name
