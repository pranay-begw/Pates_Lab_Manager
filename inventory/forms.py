from django import forms
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed
from django.forms import inlineformset_factory

class Add_Inventory_Form(forms.ModelForm):
    new_quantity = forms.IntegerField(
        required = False, 
        widget=forms.HiddenInput(), 
        initial=0)
    existing_name = forms.CharField(
        max_length=255, 
        required = False)
    class Meta:
        model = Inventory_Equipment
        fields = "__all__"

class Remove_Inventory_Form(forms.ModelForm):
    quantity_to_remove = forms.IntegerField(
        required = False, 
        widget=forms.HiddenInput(), 
        initial=0)
    equipment_name = forms.CharField(
        max_length=255, 
        required = False)
    class Meta:
        model = Inventory_Equipment
        fields = "__all__"

class New_Practical_Form(forms.ModelForm):
    class Meta:
        model = Practical
        fields = ('practical_name',)

Add_Practical_Form = inlineformset_factory(
    Practical,
    Practical_Equipment_Needed,
    fields=['equipment_needed','equipment_quantity'],
    can_delete = False)

# class Practical_Equipment_Needed_Formset(forms.ModelForm):
#     class Meta:
#         model = Practical_Equipment_Needed
#         fields = 

    # #add validation function
    # def clean_field(self):
    #     print ('hola from validation')
    #     data = self.cleaned_data['new_quantity']
    #     if not data:
    #         data = 0