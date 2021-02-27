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
     path("AddPractical/<int:id>", views.add_new_practical, name="add_new_practical"),
     path("NameNewPractical/", views.name_new_practical, name="name_new_practical"),
     path("EditPractical/", views.edit_practical, name="edit_practical"),
     path("ViewInventory/", views.view_inventory, name="view_inventory"),

     # new urls added to be able to edit the inventory equipment - based on their ID
     path("EditInventory/<int:id>", views.edit_inventory, name="edit_inventory"),
     path("Update/<int:id>", views.update, name="update"),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)