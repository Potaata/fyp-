from django.contrib import admin
from . import models
from .models import Ingredients

# Register models.
admin.site.register(models.Recipe)

admin.site.register(models.Profile)

@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    fields = ('ingredient_name', 'approved')