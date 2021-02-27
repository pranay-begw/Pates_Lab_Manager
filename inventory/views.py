from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed
from .forms import Add_Inventory_Form, Remove_Inventory_Form, Add_Practical_Formset, New_Practical_Form
from django.forms import inlineformset_factory
# Create your views here.

def homepage(response):
    return render(response, 'main/HomePage.html', {})

#function to delete a certain quantity of the selected equipment_name
def report_loss(request):
    equipment_name = Inventory_Equipment.objects.all()  # querys all the data from the inventory table into a queryset - used to render the dropdown
    if request.method == "POST": #checks if data is being SENT to template
        form = Remove_Inventory_Form(request.POST) #holds all the information from our form. 
        # When submit is clicked this gets a dictionary of all attributes and inputs, creates a new form with all values you entered.
        if form.is_valid(): #check if data entered in the form meets the constraints for forms.py file
            if (form.cleaned_data.get("quantity_to_remove") is not None): # use is not null instead
                equipment_name_selected = form.cleaned_data.get("equipment_name")
                # below line querys the quantity existing in the database
                exisitng_quantity = Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity')[0]['total_quantity']
                new_quantity = exisitng_quantity - form.cleaned_data.get("quantity_to_remove")  #subtract the quantity
                Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity').update(total_quantity = new_quantity)
            return redirect('/ViewInventory')
            # link to a page which shows the full table inventory
    else: #basically if method is GET
        form = Remove_Inventory_Form()
    return render(request, 'main/LossOrBreakReport.html', {'form': form, 'equipment_names': equipment_name})

def add_new_to_inventory(request):
    equipment_name = Inventory_Equipment.objects.all() #gets all the equipment stored in the inventory table of the db
    if request.method == "POST": # checks if data is being SENT/POSTED to the template

        form = Add_Inventory_Form(request.POST, request.FILES) #holds all the information from our form. 
        #When submit is clicked this gets a dictionary of all attributes and inputs, creates a new form with all values you entered.

        if form.is_valid(): #built-in menthod to verify the constraints in forms.py file

            if (form.cleaned_data.get("new_quantity") is not None): # checks if the field to ADD to existing qty is blank or not
                equipment_name_selected = form.cleaned_data.get("existing_name")
                print(equipment_name_selected)  #for debugging purposes
                exisitng_quantity = Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity')[0]['total_quantity']
                print(exisitng_quantity)    #for debugging purposes
                new_quantity = exisitng_quantity + form.cleaned_data.get("new_quantity")    #adds the user entered qty to exisitng_qty
                Inventory_Equipment.objects.filter(name = equipment_name_selected).values('total_quantity').update(total_quantity = new_quantity)
                print (new_quantity)    #for debugging purposes
            #add else here and check
            else:
                form.save() # if the qty to add is blank, saves the botton part of the form, creating a new record in database
            return redirect('/ViewInventory')   #displays the new record in a table - this was added later
            # link to a page which shows the full table inventory
    else: #basically if method is GET
        form = Add_Inventory_Form()
    # below line contains the context being sent to the template AddToInventory.html
    return render(request, 'main/AddToInventory.html', {'form': form, 'equipment_names': equipment_name})

# function to get all records from the inventory table and store them in a context dictionary
def view_inventory(response):
    inventory_obj = Inventory_Equipment.objects.all()   #querys every single record into this identifier
    return render(response,"main/ViewInventory.html", {'inventory_obj': inventory_obj}) #template rendered & inventory_obj passed as context to template
    
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
            new_name = form.cleaned_data.get('name_new_practical')
            
        new_practical = Practical.objects.create(practical_name = new_name)    
        new_id = Practical.objects.filter(practical_name= new_name).values('id')[0]['id']
        print (str(new_id))
            # need to get and use id of latest added object
        practical = Practical.objects.get(pk = new_id)
        return redirect('/AddPractical/%d'%new_id)
    else:
        form = New_Practical_Form()
    return render(request, 'main/NewPractical.html', {'form': form, 'practical': practical})

#formset is saving incorrectly
def add_new_practical(request, id):
    if (Practical_Equipment_Needed.objects.filter(practical_id = id).count()) == 0:
        new_practical_details = Practical_Equipment_Needed()
    else:
        print ('Exists')
        # redirect to edit practical page
    #new_practical = Practical.objects.get(id=id)
    if (request.method == 'POST'):
        #formset = Add_Practical_Formset(request.POST, queryset = Practical_Equipment_Needed.objects.filter(practical__id = id))
        formset = Add_Practical_Formset(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.practical_id  = id
                instance.save()
            return redirect('/AddPractical/%d'%id) #return to the same page after save to be able to add more equipment
    formset = Add_Practical_Formset(queryset = Practical_Equipment_Needed.objects.filter(practical__id = id))
    return render(request, 'main/AddNewPractical.html', {'formset': formset})

def edit_practical(response):
    return render(response, 'main/EditPractical.html', {})

# def add_new_practical(request):
#     if id:
#         practical = Practical.objects.get(id=id)  # if this is an edit form, replace the author instance with the existing one
#     else:
#         practical = Practical()

#     form = New_Practical_Form(instance=practical)
#     formset = Add_Practical_Form(instance = practical)
    
#     if (request.method == "POST"):
#         form = New_Practical_Form(request.POST)

#         if id: 
#             form = New_Practical_Form(request.POST, instance=practical)

#         formset = Add_Practical_Form(request.POST)

#         if form.is_valid():
#             new_practical_obj = form.save(commit=False)
#             formset = Add_Practical_Form(request.POST, instance=new_practical_obj)

#             if formset.is_valid():
#                 new_practical_obj.save()
#                 formset.save()
#                 return redirect('/AddPractical')

#     return render(request, 'main/AddNewPractical.html', {'formset': formset, 'form': form})
    