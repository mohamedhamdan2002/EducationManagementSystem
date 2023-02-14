from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser

def login_view(request):
    if request.POST:
        if request.user.is_authenticated:
            return redirect('pages:home')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        username = CustomUser.objects.get(email__iexact=email).username
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