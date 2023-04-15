# Generated by Django 4.1.7 on 2023-03-18 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_recipe_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='ingredient_name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(default=1, related_name='ingredients', to='accounts.ingredients'),
        ),
    ]
