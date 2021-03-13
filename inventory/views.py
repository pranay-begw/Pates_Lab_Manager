from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory_Equipment, Practical, Practical_Equipment_Needed, Room, Staff, Lesson, Period
from .forms import Add_Inventory_Form, Remove_Inventory_Form, Add_Practical_Formset, New_Practical_Form, Select_Practical_Form, Book_Lesson_Form
from django.forms import inlineformset_factory
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.

# homepage function needed to book a practical
def homepage(request):
    practical_list = Practical.objects.all()
    room_list = Room.objects.all()
    period_numbers = Period.objects.all()
    staff_list = Staff.objects.all()
    # get staff from the person the name of user who has logged in

    if request.method == "POST":
        form = Book_Lesson_Form(request.POST)
        if form.is_valid():
            booking_details = {
                'staff': '', 
                'period_time': '', 
                'date': '', 
                'practical_booking': '', 
                'room': '', 
                'number_students': '',}

            staff_name = form.cleaned_data.get('staff')
            staff_obj = Staff.objects.filter(staff_name=staff_name)[0]
            booking_details['staff'] = staff_obj

            period_number = form.cleaned_data.get('period_time')
            period_obj = Period.objects.filter(period_number= period_number)[0]
            booking_details['period_time'] = period_obj

            booking_date = form.cleaned_data.get('date')
            booking_details['date'] = booking_date

            practical_to_book = form.cleaned_data.get('practical_booking')
            practical_booking_obj = Practical.objects.filter(practical_name=practical_to_book)[0]
            booking_details['practical_booking'] = practical_booking_obj

            room_to_book = form.cleaned_data.get('room')
            room_obj = Room.objects.filter(room_name = room_to_book)[0]
            booking_details['room'] = room_obj

            booking_details['number_students'] = form.cleaned_data.get('number_students')

            # Add checks to see if a booking already exists
            if (Lesson.objects.filter(date=booking_details['date'], period_time=booking_details['period_time'], room=booking_details['room']).exists()):
                messages.info(request, 'A LESSON IN THIS ROOM FOR THIS TIME AND DATE EXISTS!')
            elif (Lesson.objects.filter(staff=booking_details['staff'], date=booking_details['date'], period_time=booking_details['period_time']).exists()):
                 messages.info(request, 'Selected teacher will be busy')
            else:
                # add clause such that it saves only if total calculated equipment is available.
                equipment_names, equipment_quantities = calculate_total_equipment(booking_details)
                message = create_message(equipment_names, equipment_quantities)
                email_message(message)
                Lesson.objects.create(
                    staff=booking_details['staff'], 
                    period_time=booking_details['period_time'], 
                    date=booking_details['date'], 
                    practical_booking=booking_details['practical_booking'], 
                    room=booking_details['room'], 
                    number_students=booking_details['number_students'])
    
            #FORM WORKS NEED TO SORT OUT TEMPLATE
    else:
        form = Book_Lesson_Form()
    return render(request, 'main/HomePage.html', {'form': form, 'practical_list':practical_list, 'room_list': room_list, 'period_numbers': period_numbers, 'staff_list': staff_list})

def calculate_total_equipment(booking_details):
    number_students = booking_details['number_students']
    practical_to_book = booking_details['practical_booking']
    practical_equipment = 0
    equipment_names_list = []
    equipment_quantities_list = []
    practical_id = int(Practical.objects.filter(practical_name = practical_to_book).values('id')[0]['id']) # id of practical
    equipments = Practical_Equipment_Needed.objects.filter(practical_id=practical_id).values('equipment_needed_id') #list of dictionaries that stores ID of each equipment
    # need to retrive name of equipment and their quanities
    for i in range (0, len(equipments)):

        # creating lists which store the name and quanities of each equipment needed in a practical
        equipment_name = Inventory_Equipment.objects.get(id = equipments[i]['equipment_needed_id']).name
        equipment_names_list.append(equipment_name)

        equipment_quantities = Practical_Equipment_Needed.objects.get(equipment_needed_id=equipments[i]['equipment_needed_id'], practical_id=practical_id).equipment_quantity
        equipment_quantities_list.append(equipment_quantities)
    
    print (equipment_names_list)
    print (equipment_quantities_list)

    total_equipment_needed = [i * number_students for i in equipment_quantities_list]
    print (total_equipment_needed)

    return total_equipment_needed, equipment_names_list

def create_message(equipment_names, equipment_quantities):
    message_text = ''
    for i in range (0, len(equipment_names)):
        name_quantity_pair = ''
        name_quantity_pair = str(equipment_names[i]) + ' ' + str(equipment_quantities[i]) + '\n'
        message_text += name_quantity_pair

    print (message_text)
    return message_text

def email_message(message):
        send_mail(
            'Practical Request',
            message,
            '14pbegwani@patesgs.org',
            ['pranaybegwani@gmail.com'],
            fail_silently=False,
        )

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