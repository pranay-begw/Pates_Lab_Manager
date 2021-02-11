from django import forms
from .models import Inventory_Equipment

class Add_Inventory_Form(forms.ModelForm):
    new_quantity = forms.IntegerField(required = False, widget=forms.HiddenInput(), initial=0)
    existing_name = forms.CharField(max_length=255, required = False)
    class Meta:
        model = Inventory_Equipment
        fields = "__all__"

class Remove_Inventory_Form(forms.ModelForm):
    quantity_to_remove = forms.IntegerField(required = False, widget=forms.HiddenInput(), initial=0)
    equipment_name = forms.CharField(max_length=255, required = False)
    class Meta:
        model = Inventory_Equipment
        fields = "__all__"


    # #add validation function
    # def clean_field(self):
    #     print ('hola from validation')
    #     data = self.cleaned_data['new_quantity']
    #     if not data:
    #         data = 0