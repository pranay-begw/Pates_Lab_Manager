from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views # . is from 'this app' import views

urlpatterns = [
     path("", views.homepage, name="home"), 
     #name must be same as the function name in the views.py.
     #The path('') in the urls.py of mysite looks for the same path in '' and then renders the page which follows that
     path("LossReport/", views.report_loss, name="loss_report_page"),
     path("AddInventory/", views.add_new_to_inventory, name="add_new_to_inventory"),

     # below is link to the page that helps adding new equipment to the inventory
     path("AddPractical/<int:id>", views.add_new_practical, name="add_new_practical"),
     # below is link to the page that allows user to create a new practical. This page leads to the above url
     path("NameNewPractical/", views.name_new_practical, name="name_new_practical"),

     # the url which lead to the page needed to select a practical to edit
     path("SelectPractical/", views.select_practical_to_edit, name="select_practical_to_edit"),
     # the url which leads to the page to edit details of the practical with id - id - in the Practical table
     path("EditPractical/<int:id>", views.edit_practical, name="edit_practical"),
     
     path("ViewInventory/", views.view_inventory, name="view_inventory"),

     # new urls added to be able to edit the inventory equipment - based on their ID
     path("EditInventory/<int:id>", views.edit_inventory, name="edit_inventory"),
     path("Update/<int:id>", views.update, name="update"),

     path("Delete/<int:id>", views.delete_inventory_item, name="delete_equipment"),

     path("BookingHistory/", views.booking_history, name="booking_history"),

     path('login/', views.loginPage, name="login"),
     path('logout/', views.logoutUser, name="logout"),
     path('register/', views.register, name="register"),
     
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)