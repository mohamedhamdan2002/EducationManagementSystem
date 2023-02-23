from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_only



@login_required
@admin_only
def admin_home_view(request):
    return render(request,'staff/home.html')
@login_required
def home_view(request):
    return render(request, 'index.html', {})

  