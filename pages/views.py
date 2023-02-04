from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse



def home_view(request):
    name = 'Ebraheem'
    HTML_TEXT = f"""
        <h1>Hi there i'm {name} and i just starting my project
    """
    return HttpResponse(HTML_TEXT)
