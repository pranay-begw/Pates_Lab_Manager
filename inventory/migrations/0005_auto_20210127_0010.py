# Generated by Django 3.1.3 on 2021-01-27 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20210125_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_equipment',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
