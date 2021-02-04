from django.db import models

Room_Num = (
    ('Room 1', 'Room 1'),
    ('Room 2', 'Room 2'),
    ('Room 3', 'Room 3'),
    ('Room 4', 'Room 4'),
    ('Room 5', 'Room 5'),
)

#blank = True : Not Required
#null = True : Stores some value as NULL if left empty

class Inventory_Equipment(models.Model):
    id = models.IntegerField(primary_key=True, null=False, default=0)
    name = models.CharField(max_length=255, null=False, default="Name this Equipment")
    total_quantity = models.IntegerField(null=False)
    quantity_new = models.IntegerField(null=True)
    location = models.CharField(max_length=20, default='Physics Office', choices=Room_Num)
    img_reference = models.ImageField(null=True, blank=True)

    class Meta:
        db_table="inventory"

    def __str__(self):
        return self.name

# Need to figure out auto increase id
# Need to figure out image upload to db
# Show table when changes made
# remove equipment

# less modularizing the app - making it complicated - add all tables in here and link them properly - one by one though
# first complete inventory

# class Practical(models.Model):
#     pass

# class Lessons(models.Model):
#     pass

# class Rooms(models.Model):
#     pass

# class Staff(models.Model):
#     pass