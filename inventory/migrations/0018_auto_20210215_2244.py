# Generated by Django 3.1.3 on 2021-02-15 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20210211_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_equipment',
            name='img_reference',
            field=models.ImageField(blank=True, default='images_uploaded/default.jpg', null=True, upload_to='images_uploaded/'),
        ),
    ]