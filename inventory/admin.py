from django.contrib import admin
from inventory.models import Inventory_Equipment, Practical, Practical_Equipment_Needed, Room, Staff, Period, Lesson

# Register your models here.

admin.site.register(Inventory_Equipment)
admin.site.register(Practical)
admin.site.register(Practical_Equipment_Needed)
admin.site.register(Room)
admin.site.register(Staff)
admin.site.register(Period)
admin.site.register(Lesson)
