# Generated by Django 3.1.3 on 2021-03-05 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_auto_20210305_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='staff',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.staff'),
        ),
    ]