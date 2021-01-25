from django.db import models

Room_Num = (
    ('Room 1', 'Room 1'),
    ('Room 2', 'Room 2'),
    ('Room 3', 'Room 3'),
    ('Room 4', 'Room 4'),
    ('Room 5', 'Room 5'),
)


class Inventory_Equipment(models.Model):
    id = models.IntegerField(primary_key=True, null=False, default=0)
    name = models.CharField(max_length=255, null=False, default="Name this Equipment")
    total_quantity = models.IntegerField(null=False)
    location = models.CharField(max_length=20, default='Physics Office', choices=Room_Num)
    img_reference = models.ImageField(null=True, blank=True)

    class Meta:
        db_table="inventory"


# Need to figure out auto increase id
# Need to figure out image upload to db
# Show table when changes made
# remove equipment