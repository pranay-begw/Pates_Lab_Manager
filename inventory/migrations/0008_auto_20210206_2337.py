# Generated by Django 3.1.3 on 2021-02-06 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_remove_inventory_equipment_quantity_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_equipment',
            name='id',
            field=models.IntegerField(blank=True, default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inventory_equipment',
            name='location',
            field=models.CharField(blank=True, choices=[('Room 1', 'Room 1'), ('Room 2', 'Room 2'), ('Room 3', 'Room 3'), ('Room 4', 'Room 4'), ('Room 5', 'Room 5')], default='Physics Office', max_length=20),
        ),
        migrations.AlterField(
            model_name='inventory_equipment',
            name='name',
            field=models.CharField(blank=True, default='Name this Equipment', max_length=255),
        ),
        migrations.AlterField(
            model_name='inventory_equipment',
            name='total_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
