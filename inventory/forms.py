from django import forms
from .models import Inventory_Equipment

class Add_Inventory_Form(forms.ModelForm):
    class Meta:
        model = Inventory_Equipment
        fields = "__all__"
