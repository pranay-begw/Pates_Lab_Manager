from django.urls import path

from . import views # . is from 'this app' import views

urlpatterns = [
     path("", views.homepage, name="home"), #name must be same as the function name in the views.py, the path('') in the urls.py of mysite looks for the same path in '' and then renders the page which follows that
     path("LossReport/", views.report_loss, name="loss_report_page"),
     path("AddInventory/", views.add_to_inventory, name="add_to_inventory"),
     path("AddPractical/", views.add_new_practical, name="add_new_practical"),
      path("EditPractical/", views.edit_practical, name="edit_practical"),
]