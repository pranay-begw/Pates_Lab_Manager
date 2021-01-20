from django.db import models


class Inventory_Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, default="Name this Equipment")
    total_quantity = models.IntegerField(null=False)
    location = models.CharField(max_length=20, default='Physics Office')
    img_reference = models.ImageField(null=True)

    class Meta:
        db_table="inventory"
