from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage(response):
    return render(response, 'HomePage.html', {})
    