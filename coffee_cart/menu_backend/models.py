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

    def __str__(self):
        self.item.name

class Snack(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    drinks = models.ManyToManyField(Drink)

    def __str__(self):
        self.item.name
    
