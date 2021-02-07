from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory_Equipment
from .forms import Add_Inventory_Form
# Create your views here.

def homepage(response):
    return render(response, 'main/HomePage.html', {})

def report_loss(response):
    return render(response, 'main/LossOrBreakReport.html', {})

def add_new_to_inventory(request):
    practical_name = Inventory_Equipment.objects.all()
    if request.method == "POST":
        form = Add_Inventory_Form(request.POST, request.FILES) #holds all the information from our form. When submit is clicked this gets a dictionary of all attributes and inputs, creates a new form with all values you entered.
        if form.is_valid():
            # NEED TO GET THESE LINES BELOW TO WORK

            if ( form.cleaned_data.get("new_quantity") != 0 ): # use is not null instead
                practical_name_selected = form.cleaned_data.get("existing_name")
                print(practical_name_selected)
                exisitng_quantity = Inventory_Equipment.objects.filter(name = practical_name_selected).values('total_quantity')[0]['total_quantity']
                new_quantity = exisitng_quantity + form.cleaned_data.get("new_quantity")
                Inventory_Equipment.objects.filter(name = practical_name_selected).values('total_quantity').update(total_quantity = new_quantity)
                print (new_quantity)
            form.save()
            return redirect('/AddInventory')
            # link to a page which shows the full table inventory
    else: #basically if method is GET
        form = Add_Inventory_Form()
    return render(request, 'main/AddToInventory.html', {'form': form, 'practical_names': practical_name})


###################################################################################################################################
    # in the above code, retrieve the record of dropdown selection and add the quantity_new value to exisitng qty 
####################################################################################################################################

def view_inventory(request):
    inventory_obj = Inventory_Equipment.objects.all()
    return render(request,"main/ViewInventory.html", {'inventory_obj': inventory_obj})

def add_new_practical(response):
    return render(response, 'main/AddNewPractical.html', {})

def edit_practical(response):
    return render(response, 'main/EditPractical.html', {})