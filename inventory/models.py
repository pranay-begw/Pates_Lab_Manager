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


# the count of the field below must be equal to the count of columns in db table - therefore deleting quantity_ne
class Inventory_Equipment(models.Model):
    id = models.IntegerField(primary_key=True, null=False, default=0)
    name = models.CharField(max_length=255, null=False, default="Name this Equipment") # might have to divide this into name from frop down and new name
    total_quantity = models.IntegerField(null=True) # qty to add an entirely new equipment - bottom of form
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