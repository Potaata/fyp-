# Generated by Django 4.1.7 on 2023-03-18 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredients',
            name='ingredient_id',
            field=models.IntegerField(default=1),
        ),
    ]
