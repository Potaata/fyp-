from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.apps import AppConfig
from django.conf import settings
from django.db.models import BigAutoField


class AccountsConfig(AppConfig):
    default_auto_field = BigAutoField

class Ingredients(models.Model):
    ingredient_name = models.CharField(max_length=250, unique=True)
    ingredient_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f'{self.ingredient_name}'
    
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE, default=1)
    servings = models.IntegerField(default=1)
    estimated = models.CharField(max_length=50)
    favourites = models.ManyToManyField(User, related_name='favourites', blank=True)
    photo = models.ImageField(upload_to="photos/", blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("recipes-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.recipe_name}'
    

