# Generated by Django 3.2.18 on 2023-04-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_recipe_favourites'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]
