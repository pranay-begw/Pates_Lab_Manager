from django.contrib import admin
from inventory.models import Inventory_Equipment, Practical, Practical_Equipment_Needed

# Register your models here.

admin.site.register(Inventory_Equipment)
admin.site.register(Practical)
admin.site.register(Practical_Equipment_Needed)
