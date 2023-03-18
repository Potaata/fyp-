# Generated by Django 4.1.7 on 2023-03-18 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_ingredients_ingredient_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ForeignKey(db_column='ingredient_name', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.ingredients'),
        ),
    ]