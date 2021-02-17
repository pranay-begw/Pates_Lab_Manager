from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed
from .forms import Add_Inventory_Form, Remove_Inventory_Form, Add_Practical_Form, New_Practical_Form
from django.forms import inlineformset_factory
# Create your views here.

def homepage(response):
    return render(response, 'main/HomePage.html', {})

def report_loss(request):
    equipment_name = Inventory_Equipment.objects.all()
    if request.method == "POST":
        form = Remove_Inventory_Form(request.POST) #holds all the information from our form. When submit is clicked this gets a dictionary of all attributes and inputs, creates a new form with all values you entered.
        if form.is_valid():
            if (form.cleaned_data.get("quantity_to_remove") is not None): # use is not null instead
                equipment_name_selected = form.cleaned_data.get("equipment_name")
                exisitng_quantity = Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity')[0]['total_quantity']
                new_quantity = exisitng_quantity - form.cleaned_data.get("quantity_to_remove")
                Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity').update(total_quantity = new_quantity)
            return redirect('/ViewInventory')
            # link to a page which shows the full table inventory
    else: #basically if method is GET
        form = Remove_Inventory_Form()      
    return render(request, 'main/LossOrBreakReport.html', {'form': form, 'equipment_names': equipment_name})

def add_new_to_inventory(request):
    equipment_name = Inventory_Equipment.objects.all()
    if request.method == "POST":
        form = Add_Inventory_Form(request.POST, request.FILES) #holds all the information from our form. When submit is clicked this gets a dictionary of all attributes and inputs, creates a new form with all values you entered.
        if form.is_valid():
            # NEED TO GET THESE LINES BELOW TO WORK
            # CODE SUCH THAT THE FIRST PART OF THIS FORM IS NOT REQUIRED WHEN ADDIN TOTALLY NEW STUFF AND VICE VERSA

            if (form.cleaned_data.get("new_quantity") is not None): # use is not null instead
                equipment_name_selected = form.cleaned_data.get("existing_name")
                print(equipment_name_selected)
                exisitng_quantity = Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity')[0]['total_quantity']
                print(exisitng_quantity)
                new_quantity = exisitng_quantity + form.cleaned_data.get("new_quantity")
                Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity').update(total_quantity = new_quantity)
                print (new_quantity)
            #add else here and check
            else:
                form.save()
            return redirect('/ViewInventory')
            # link to a page which shows the full table inventory
    else: #basically if method is GET
        form = Add_Inventory_Form()
    return render(request, 'main/AddToInventory.html', {'form': form, 'equipment_names': equipment_name})

def view_inventory(response):
    inventory_obj = Inventory_Equipment.objects.all()
    return render(response,"main/ViewInventory.html", {'inventory_obj': inventory_obj})
    
def edit_inventory(request, id):
    inventory_obj = Inventory_Equipment.objects.get(id = id)
    return render(request,'main/EditInventoryDetails.html', {'inventory_obj': inventory_obj})

# NEED to NOT create a new record if saved. try the update() method?
def update(request, id):  
    inventory_obj = Inventory_Equipment.objects.get(id = id)  
    if (request.method == 'POST'):
        form = Add_Inventory_Form(request.POST or None, request.FILES or None, instance = inventory_obj)
        if form.is_valid():
            form.save()
        return redirect("/ViewInventory")
    else: #basically if method is GET
        form = Remove_Inventory_Form()
    return render(request, 'main/EditInventoryDetails.html', {'inventory_obj': inventory_obj })

def name_new_practical(request):
    practical = Practical.objects.all()
    if (request.method == 'POST'):
        form = New_Practical_Form(request.POST)
        if form.is_valid():
            form.save()
        name = str(form.cleaned_data.get('practical_name'))
        practical_id = int(Practical.objects.filter(practical_name = name).values('id')[0]['id'])
        #return redirect('/')
    else:
        form = New_Practical_Form()
    
    return render(request, 'main/NewPractical.html', {'form': form, 'practical': practical})

def add_new_practical(request, id):
    equipment_name = Inventory_Equipment.objects.all()
    new_practical = Practical.objects.get(id=id)
    formset = Add_Practical_Form(queryset=Practical_Equipment_Needed.objects.none(), instance=new_practical)
    if (request.method == 'POST'):
        formset = Add_Practical_Form(request.POST, instance=new_practical)
        if formset.is_valid():
            formset.save()
            return redirect('/AddInventory')
    
    formset = Add_Practical_Form()

    return render(request, 'main/AddNewPractical.html', {'formset': formset, 'equipment_names': equipment_name})

def edit_practical(response):
    return render(response, 'main/EditPractical.html', {})