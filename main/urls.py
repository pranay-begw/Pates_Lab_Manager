from django.urls import path

from . import views # . is from 'this app' import views

urlpatterns = [
     path("", views.homepage, name="home"), #name must be same as the function name in the views.py, the path('') in the urls.py of mysite looks for the same path in '' and then renders the page which follows that
]