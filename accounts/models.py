from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.apps import AppConfig
from django.conf import settings
from django.db.models import BigAutoField
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

class AccountsConfig(AppConfig):
    default_auto_field = BigAutoField

class Ingredients(models.Model):
    ingredient_name = models.CharField(max_length=250, unique=True)
    approved = models.BooleanField("Approved", default=False)
    
    def __str__(self):
        return f'{self.ingredient_name}'
    
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ManyToManyField('Ingredients', blank=True)
    servings = models.IntegerField(default=1, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    estimated = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    author = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    favourites = models.ManyToManyField(User, related_name="favourite", blank=True)
  
    def get_absolute_url(self):
        return reverse("recipes-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.recipe_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                    related_name="followed_by",
                    symmetrical=False,
                    blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="photos/")
    def __str__(self):
        return f'{self.user.username}'

# create profile when new user sign up
def created_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(created_profile, sender=User)