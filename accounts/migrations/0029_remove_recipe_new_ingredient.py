# Generated by Django 3.2.18 on 2023-04-04 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_recipe_new_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='new_ingredient',
        ),
    ]
