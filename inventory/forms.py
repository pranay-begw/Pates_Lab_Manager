from django import forms
from .models import Inventory_Equipment

class Add_Inventory_Form(forms.ModelForm):
    new_quantity = forms.IntegerField(required = False)
    existing_name = forms.CharField(max_length=255, required = False)
    class Meta:
        model = Inventory_Equipment
        fields = "__all__"