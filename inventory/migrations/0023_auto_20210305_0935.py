# Generated by Django 3.1.3 on 2021-03-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_lesson_period_room_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='number_students',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inventory_equipment',
            name='total_quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='practical_equipment_needed',
            name='equipment_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
