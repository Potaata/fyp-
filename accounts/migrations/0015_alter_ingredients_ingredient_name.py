# Generated by Django 3.2.18 on 2023-03-29 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='ingredient_name',
            field=models.CharField(max_length=250),
        ),
    ]
