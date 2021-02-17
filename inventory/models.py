from django.db import models

# Room_Num = (
#     ('Select', 'Select'),
#     ('Room 1', 'Room 1'),
#     ('Room 2', 'Room 2'),
#     ('Room 3', 'Room 3'),
#     ('Room 4', 'Room 4'),
#     ('Room 5', 'Room 5'),
# )

#blank = True : Not Required
#null = True : Stores some value as NULL if left empty

# I HAVE MADE THEM ALL BLANK=TRUE -- AFTER ADDING WORKS TRY TO MAKE THEM BLANK CONDITIONALLY SUCH THAT IT IS ALLOWED ONLY IF SELECTING AN EQUIPMENT THAT EXISTS

# the count of the field below must be equal to the count of columns in db table - therefore deleting quantity_ne
class Inventory_Equipment(models.Model):
    #id = models.IntegerField(primary_key=True, null=False, blank=True)
    name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        default="Name this Equipment") # might have to divide this into name from frop down and new name
    total_quantity = models.IntegerField(
        null=True, 
        blank=True) # qty to add an entirely new equipment - bottom of form
    location = models.CharField(
        max_length=20, 
        default='Physics Office', 
        blank=True)
    img_reference = models.ImageField(
        null=True, 
        blank=True, 
        upload_to='images_uploaded/', 
        default='images_uploaded/default.jpg')

    class Meta:
        db_table="inventory"

    def __str__(self):
        return self.name

    #add validation functions

class Practical(models.Model):
    practical_name = models.CharField(
        max_length=30, 
        blank=True)
    equipment_needed = models.ManyToManyField(
        'Inventory_Equipment', 
        blank=True, 
        through='Practical_Equipment_Needed')
    
    class Meta:
        db_table="practical"

    def __str__(self):
        return self.practical_name

class Practical_Equipment_Needed(models.Model):
    equipment_needed = models.ForeignKey(
        'Inventory_Equipment', 
        on_delete=models.CASCADE)
    practical = models.ForeignKey(
        'Practical', 
        on_delete=models.CASCADE)
    equipment_quantity = models.IntegerField(
        default=0)

    class Meta:
        db_table="practical_equipment_needed"

    def __str__(self):
        return self.practical.practical_name



# class Practical(models.Model):
#     id = models.IntegerField(primary_key=True, null=False, blank=True)
#     practical_name = models.CharField(max_length=255, blank=True, null=True, default='Unnamed Practical')
#     equipment_needed = models.ManyToManyField(Inventory_Equipment, )    

# Need to figure out auto increase id
# Need to figure out image upload to db
# Show table when changes made
# remove equipment

# less modularizing the app - making it complicated - add all tables in here and link them properly - one by one though
# first complete inventory

# class Lessons(models.Model):
#     pass

# class Rooms(models.Model):
#     pass

# class Staff(models.Model):
#     pass