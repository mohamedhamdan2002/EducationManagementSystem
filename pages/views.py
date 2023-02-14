from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse



def home_view(request):
    return render(request, 'index.html', {})
