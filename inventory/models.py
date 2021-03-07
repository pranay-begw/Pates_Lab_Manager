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


# class to represent the INVENTORY table in the database
class Inventory_Equipment(models.Model):
    #id = models.IntegerField(primary_key=True, null=False, blank=True)
    # The above field now not in the code so that the records for each equipment are unique
    name = models.CharField(
        max_length=255,     #maximum length of input
        blank=True,         #the field can be blank
        null=True,          #the field can be null
        default="Name this Equipment")  # the defualt value if it is left blank
    total_quantity = models.PositiveIntegerField(
        null=True, 
        blank=True)
    location = models.CharField(
        max_length=20, 
        default='Physics Office', 
        blank=True)
    img_reference = models.ImageField(
        null=True, 
        blank=True, 
        upload_to='images_uploaded/',   #the location of where to store uploaded images
                                        #currently the location is local device
        default='images_uploaded/default.jpg')  #the default image stored if no image is uploaded by user

    class Meta:
        db_table="inventory"    #name of the table in the database to which this model links to

    def __str__(self):
        return self.name    #when queryed, the 'name' is returned

    #add validation functions - validation is a step i will do after barebones of the program are made

# Table to store list of all the practical - just their names
class Practical(models.Model):
    practical_name = models.CharField(
        max_length=100, 
        blank=True)
    equipment_needed = models.ManyToManyField(  # this is used to link to the link table to normalize the many to many relationship
        'Inventory_Equipment', # name of the table to which this has a many to many relationship with
        blank=True, 
        through='Practical_Equipment_Needed')   # name of the link table to normalize the many to many relationship
    
    class Meta:
        db_table="practical"

    def __str__(self):
        return self.practical_name

# Table to store the equipment needed in every practical and their quantities
class Practical_Equipment_Needed(models.Model):
    equipment_needed = models.ForeignKey(   # a foreign key of the inventory table to store the equipment
        'Inventory_Equipment', # table of which this is a foreign key
        on_delete=models.CASCADE)   # needed to reflect any deletions all across the database 
    practical = models.ForeignKey(  #foreign key of the Practical table
        'Practical', 
        on_delete=models.CASCADE)
    equipment_quantity = models.PositiveIntegerField(   # integer field needed to store the quantity of an equipment
        default=0)  # the quantity if no number is entered by the user

    class Meta:
        db_table="practical_equipment_needed"

    def __str__(self):
        return self.practical.practical_name

class Staff(models.Model):
    staff_name = models.CharField(max_length=255)# something like a dropdown of the staff names from the database

    class Meta:
        db_table="Staff"

    def __str__(self):
        return self.staff_name

class Room(models.Model):
    room_name = models.CharField(max_length=30)#something like a dropdown of all rooms from the database...

    class Meta:
        db_table="Room"

    def __str__(self):
        return self.room_name

class Period(models.Model):
    PERIOD_NUMBER_CHOICES = [
            ('Lesson 1','Lesson 1'),
            ('Lesson 2','Lesson 2'),
            ('Lesson 3','Lesson 3'),
            ('Lesson 4','Lesson 4'),
            ('Lesson 5','Lesson 5'),
        ]

    period_number = models.CharField(
                                    choices=PERIOD_NUMBER_CHOICES,
                                    max_length = 10)

    class Meta:
        db_table = 'period_number'
    
    def __str__(self):
        return self.period_number
    

class Lesson(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default= 1, null=True, blank=True)
    period_time = models.ForeignKey(Period, on_delete=models.CASCADE)
    date = models.DateField()
    practical_booking = models.ForeignKey(Practical, on_delete=models.CASCADE)#or is it fk for Practical_Equipment_Needed
    room = models.ForeignKey(Room, on_delete=models.CASCADE)#location of lesson
    number_students = models.PositiveIntegerField(default = 0)

    class Meta:
        db_table = 'Lesson_Bookings'

    # def __str__(self):
    #     return self.practical_booking

# class Lessons(models.Model):
#     pass

# class Rooms(models.Model):
#     pass

# class Staff(models.Model):
#     pass