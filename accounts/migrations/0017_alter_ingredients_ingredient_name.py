# Generated by Django 3.2.18 on 2023-03-30 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_ingredients_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='ingredient_name',
            field=models.CharField(max_length=250),
        ),
    ]
