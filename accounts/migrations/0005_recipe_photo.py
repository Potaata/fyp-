# Generated by Django 4.1.7 on 2023-03-18 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_recipe_favourites_alter_ingredients_ingredient_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/'),
        ),
    ]