from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage(response):
    return render(response, 'main/HomePage.html', {})

def report_loss(response):
    return render(response, 'main/LossOrBreakageReport.html', {})
    