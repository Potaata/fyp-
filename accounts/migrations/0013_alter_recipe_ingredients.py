# Generated by Django 3.2.18 on 2023-03-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_recipe_new_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.Ingredients'),
        ),
    ]
