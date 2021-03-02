from django import forms    # importing the forms module from django
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed
# importing all the models created in models.py
from django.forms import modelformset_factory

class Add_Inventory_Form(forms.ModelForm):
    new_quantity = forms.IntegerField(# field to enter the qty needed to be added to existing equipment
        required = False, 
        widget=forms.HiddenInput(), 
        initial=0)
    existing_name = forms.CharField( # field to select the equipment to add qty to
        max_length=255, 
        required = False)
    class Meta:
        model = Inventory_Equipment # name of the model that this form represents
        fields = "__all__" # means that all attributes of the model named above will have a field

#form to report loss of equipment from inventory
class Remove_Inventory_Form(forms.ModelForm):   #name of the form to remove equipment
    quantity_to_remove = forms.IntegerField(    #integer field for the quantity that is to be removed
        required = False, 
        widget=forms.HiddenInput(), 
        initial=0)
    equipment_name = forms.CharField(   #name of the equipment to be removed from - this is rendered as a dropdown
        max_length=255, 
        required = False)
    class Meta:
        model = Inventory_Equipment # name of the model that this form is connected to
        fields = "__all__"  # means that all attributes of the model named above will have a field

class New_Practical_Form(forms.Form):
    name_new_practical = forms.CharField(max_length=100)

# form to input a single equipment and its quantity for a practical
class New_Practical_Detail_Form(forms.ModelForm):   # declaring the form
    class Meta:
        model = Practical_Equipment_Needed  # the model that this form is connected to
        fields = ('equipment_needed', 'equipment_quantity', )   # fields needed in the form

# formset which creates multiple instances of the form above
Add_Practical_Formset = modelformset_factory(   # declaring the formset
    Practical_Equipment_Needed, #the models that this formset is connected to
    New_Practical_Detail_Form   # the form (above) whose copies this formset creates
)

#Form to select the practical that the user wants to edit
class Select_Practical_Form(forms.Form):
    name_practical = forms.CharField(max_length=255) 

# Add_Practical_Formset = inlineformset_factory(  #creating the formset to input details of practical
#     Practical,  # the parent model for the form
#     Practical.equipment_needed.through, # 'through' reference/ link model for the form 
#     fields=['equipment_needed','equipment_quantity'],   #the fields needed in  the form
# )