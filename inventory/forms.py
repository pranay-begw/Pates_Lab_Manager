from django import forms    
# importing the forms module from django
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed, Lesson, Staff, Room, Period
# importing all the models created in models.py
from django.forms import modelformset_factory
# importing library to use input validation in django
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

##########################################################################################

class Add_Inventory_Form(forms.ModelForm):
    new_quantity = forms.IntegerField(  #field to enter the qty needed to be added to existing equipment
        required = False, 
        widget=forms.HiddenInput(), 
        initial=0)
    existing_name = forms.CharField(    #field to select the equipment to add qty to
        max_length=255, 
        required = False)
    class Meta:
        model = Inventory_Equipment     #name of the model that this form represents
        fields = "__all__"              #means that all attributes of the model named above will have a field

    # def check_integer_validation(value):
    #     if type(value) != int:
    #         raise forms.ValidationError({"quantity_to_remove" : "Please Enter an Integer Value"})
#validators= [check_integer_validation, ]

#form to report loss of equipment from inventory
class Remove_Inventory_Form(forms.ModelForm):   #name of the form to remove equipment
    quantity_to_remove = forms.IntegerField(    #integer field for the quantity that is to be removed
        required = True, 
        widget=forms.HiddenInput(), 
        initial=0,
        min_value=0)
        # max_value=Inventory_Equipment.objects.filter(name = equip_nam).values('total_quantity')[0]['total_quantity'],   #fix this
    equipment_name = forms.CharField(   #name of the equipment to be removed from - this is rendered as a dropdown
        max_length=255, 
        required = True)
    class Meta:
        model = Inventory_Equipment     #name of the model that this form is connected to
        fields = "__all__"              #means that all attributes of the model named above will have a field


    # def clean_equipment_name(self):
    #     quant_entered = self.cleaned_data.get("quantity_to_remove")
    #     equip_nam = self.cleaned_data.get("equipment_name")
    #     total_quant = Inventory_Equipment.objects.filter(name = equip_nam).values('total_quantity')[0]['total_quantity']
    #     if quant_entered > total_quant:
    #         raise forms.ValidationError("Cant remove more than available quantity")
    #     # elif type(quant_entered) is not int:
    #     #     raise forms.ValidationError("Enter integer quantity")
    #     return quant_entered
# def check_range(value):
#     if value < Inventory_Equipment.objects.get(name = ).total_quantity:


class New_Practical_Form(forms.Form):
    name_new_practical = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class' : 'text-box'}))
    
# form to input a single equipment and its quantity for a practical
class New_Practical_Detail_Form(forms.ModelForm):   # declaring the form
    class Meta:
        model = Practical_Equipment_Needed      #the model that this form is connected to
        fields = ('equipment_needed', 'equipment_quantity', )   # fields needed in the form

# formset which creates multiple instances of the form above
Add_Practical_Formset = modelformset_factory(   #declaring the formset
    Practical_Equipment_Needed,                 #the models that this formset is connected to
    New_Practical_Detail_Form,                  #the form (above) whose copies this formset creates
    can_delete=True                 
)

#Form to select the practical that the user wants to edit
class Select_Practical_Form(forms.Form):
    name_practical = forms.CharField(max_length=255) 

# Form to book a lesson in a particular room for some number of students
class Book_Lesson_Form(forms.Form):
    staff = forms.ModelChoiceField(
        queryset=Staff.objects.all(), 
        empty_label='Select', 
        widget=forms.Select(attrs={'class' : 'small-drop-downs'}))
    # dropdown to select staff name
    period_time = forms.ModelChoiceField(
        queryset=Period.objects.all(), 
        empty_label='Select', 
        widget=forms.Select(attrs={'class' : 'small-drop-downs'}))
    # dropdown to select choice of lesson
    date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'id': 'date-widget'}))
    # date field that display a calendar allowing the user to select a specific date
    practical_booking = forms.ModelChoiceField(
        queryset=Practical.objects.all(), 
        empty_label='Select', 
        widget=forms.Select(attrs={'id' : 'practical-list'}))
    # dropdown to select what practical to boo for
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(), 
        empty_label='Select', 
        widget=forms.Select(attrs={'class' : 'small-drop-downs'}))
    # dropdown to select room number to book
    number_students = forms.IntegerField(
        widget=forms.TextInput(attrs={'class' : 'text-boxes'}))
    # integer field to enter the number of students in the lesson being booked