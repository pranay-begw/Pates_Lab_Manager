from django.shortcuts import render
from django.http import HttpResponse
from .models import Inventory_Equipment
from .forms import Add_Inventory_Form
# Create your views here.

def homepage(response):
    return render(response, 'main/HomePage.html', {})

def report_loss(response):
    return render(response, 'main/LossOrBreakReport.html', {})
    
def add_to_inventory(response):
    if response.method == "POST":
        form = Add_Inventory_Form(response.POST) #holds all the information from our form. When submit is clicked this gets a dictionary of all attributes and inputs, creates a new form with all values you entered.
        if form.is_valid():
            form.save()
            # link to a page which shows the full table inventory
    else: #basically if method is GET
        form = Add_Inventory_Form()

    return render(response, 'main/AddToInventory.html', {})

def add_new_practical(response):
    return render(response, 'main/AddNewPractical.html', {})

def edit_practical(response):
    return render(response, 'main/EditPractical.html', {})