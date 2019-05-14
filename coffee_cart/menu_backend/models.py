from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# class Ingredient(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         self.name

class Item(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    ingredients = ArrayField(models.CharField(max_length=100))

    def __str__(self):
        self.name

class Drink(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)

    def addSnacks(self, well_with):
      snacks = Snack.objects.filter(item__name__in=well_with)
      for snack in snacks:
          self.snack_set.add(snack)
      self.save()
      return

    def __str__(self):
        self.item.name

class Snack(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    drinks = models.ManyToManyField(Drink)

    def addDrinks(self, well_with):
      drinks = Drink.objects.filter(item__name__in=well_with)
      for drink in drinks:
        self.drinks.add(drink)
      return

    def __str__(self):
        self.item.name
    
