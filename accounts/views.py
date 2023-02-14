from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from funcs.validators import validate_email
from .models import CustomUser

def login_view(request):
    if request.POST:
        if request.user.is_authenticated:
            return redirect('pages:home')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if validate_email(username):
            username = CustomUser.objects.get(email__iexact=username).username
        user = authenticate(request, username=username, password=password)
        if not user:
            return render(request, 'accounts/login.html', {'error': 'No user with this credintials'})
        login(request, user)
        return redirect('pages:home')
    return render(request, 'accounts/login.html', {})
    


def logout_view(request):  
    if request.POST:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/logout.html', {})