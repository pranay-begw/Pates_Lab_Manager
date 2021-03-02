from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed
from .forms import Add_Inventory_Form, Remove_Inventory_Form, Add_Practical_Formset, New_Practical_Form, Select_Practical_Form
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

# in both the functions below, id is the ID for the item in inventory to be edited

# function to get the record that needs to be edited and pass it to the template  
def edit_inventory(request, id):
    inventory_item = Inventory_Equipment.objects.get(id = id) # get the item with the given id from the inventory table 
    return render(request,'main/EditInventoryDetails.html', {'inventory_item': inventory_item})

# function to edit the exisiting item
def update(request, id):  
    inventory_item = Inventory_Equipment.objects.get(id = id)  # get the item with the given id from the inventory table
    if (request.method == 'POST'):  # if data is being sent to the server/POSTED to server
        # below line renders the form, Add_Inventory_Form with data already filled in - the data is the instance
        form = Add_Inventory_Form(request.POST or None, request.FILES or None, instance = inventory_item)
        if form.is_valid(): #if the form meets validation criteria
            form.save() #save updated details to the database
        return redirect("/ViewInventory")   # once completed lead the inventory table page
    else: #basically if method is GET
        form = Remove_Inventory_Form()  #empty form if GETTING the page from database 
    return render(request, 'main/EditInventoryDetails.html', {'inventory_obj': inventory_item })

# function to create new empty practical
def name_new_practical(request):
    practical = Practical.objects.all()

    if (request.method == 'POST'):  #if connection method is POST
        form = New_Practical_Form(request.POST) #creates new form to send data to server
        if form.is_valid():
            new_name = form.cleaned_data.get('name_new_practical')  #gets name of the new practical in the variable   
        new_practical = Practical.objects.create(practical_name = new_name)    # creates new practicalin the database
        new_id = Practical.objects.filter(practical_name= new_name).values('id')[0]['id']   #gets id of the newly added practical

        print (str(new_id))
        practical = Practical.objects.get(pk = new_id)  # querys the new practical using its ID to pass to template 
        return redirect('/AddPractical/%d'%new_id)  #once all tasks complete, leads to the AddPractical page to enter details of new practical
    else:
        form = New_Practical_Form() # if the method is GET, displays the empty form
    return render(request, 'main/NewPractical.html', {'form': form, 'practical': practical})

# function to add details of newly added practical to database
def add_new_practical(request, id): # ID of the newly added practical is a parameter so that equipment is added for that practical only

    if (Practical_Equipment_Needed.objects.filter(practical_id = id).count()) == 0: # checks if the practical already exists in the database
        new_practical_details = Practical_Equipment_Needed()    # if it doesn't exist, creates empty object for details
    else:
        print ('Exists')    # prints exists if practical already exists
        # redirect to edit practical page

    if (request.method == 'POST'):  # if method is POST
        formset = Add_Practical_Formset(request.POST)   # creates new empty formset to add details for the selected practical
        if formset.is_valid():
            instances = formset.save(commit=False)  # saves data but doesn't send it to the database
            for instance in instances:  # querys through every individual instance of the formset  
                instance.practical_id  = id
                instance.save() #saves individual instance to the Practical_Equipment_Needed database table
            return redirect('/AddPractical/%d'%id) #return to the same page after save to be able to add more equipment

    formset = Add_Practical_Formset(queryset = Practical_Equipment_Needed.objects.filter(practical__id = id))   # empty formset

    return render(request, 'main/AddNewPractical.html', {'formset': formset})

# function to enable user to choose the practical whose details they want to edit
def select_practical_to_edit(request):
    practical_names = Practical.objects.all()   # storing objects of all practical to render names in the dropdown on webpage

    if (request.method == 'POST'):  # if POSTING data to the backend
        form = Select_Practical_Form(request.POST)  # rendering the Select_Practical_Form needed to take input of practical name
        if form.is_valid(): # checking if form meets validation constraints
            selected_practical_name = form.cleaned_data.get('name_practical')   # storing the name selected by user in a variable
        
        id_selected  =  Practical.objects.filter(practical_name= selected_practical_name).values('id')[0]['id'] # getting id of the selected practical
        return redirect('/EditPractical/%d'%id_selected)    # redirecting user to the page needed to edit the details of the selected practical
        
    else:   # if GETTING data/information
        form = Select_Practical_Form()  # displays an empty form
    
    return render(request,'main/SelectPracticalToEdit.html', {'form': form, 'practical_names': practical_names})    #renders webpage and sends data to template

# function to edit details of practical selected using select_practical_to_add
def edit_practical(request, id):
    practical_names = Practical.objects.all()   # storing all practical objects in a queryset

    if (request.method == 'POST'):
        formset = Add_Practical_Formset(request.POST)   # renders the formset to allow user to edit practical selected
        if formset.is_valid():
            instances = formset.save(commit=False)  # commit is false so that the user can make multiple additions at the same time
            for instance in instances:  # cycle through all instances and save them individually to database
                instance.practical_id = id  # making sure instance is saved for the practical with th correct id
                instance.save()
        return redirect('/EditPractical/%d'%id) # leads to the same page to allow user to add/edit more details

     # displaying formset with existing details of practical
    formset = Add_Practical_Formset(queryset = Practical_Equipment_Needed.objects.filter(practical__id = id))
    
    return render(request, 'main/EditPractical.html', {'formset': formset, 'practical_names': practical_names})

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
    