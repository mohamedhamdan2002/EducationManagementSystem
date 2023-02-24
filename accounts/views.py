from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

from funcs.validators import validate_email
from .models import CustomUser
from .forms import LoginForm, SignupForm

def sign_up_view(request):
    form = SignupForm(request.POST or None)
    context ={
        'form': form,
    }
    if form.is_valid():
        user=form.save()
        messages.success(request,"your account has been created! you are now able to log in")
        #CustomUser.objects.create(
        #    first_name=form.cleaned_data.get('first_name'),
        #    last_name=form.cleaned_data.get('last_name'),
        #    date_of_birth=form.cleaned_data.get('date_of_birth'),
        #    email=form.cleaned_data.get('email'),
        #    username=form.cleaned_data.get('username'),
        #    password=make_password(form.cleaned_data.get('password1')),
        #)
        group=Group.objects.get(name='students')
        group.add(user)
        return redirect('accounts:login')
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('pages:home')
    #form = LoginForm(request.POST or None)
    context = {}
    #if form.is_valid():
    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        #username = form.cleaned_data.get('username')
        #password = form.cleaned_data.get('password')
        #if validate_email(username):
        #    username = CustomUser.objects.get(email__iexact=username).username
        #user = authenticate(request, username=username, password=password)
        #if user:
        #    login(request, user)
        #    return redirect('pages:home')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pages:staff-home')
        context['error'] = 'No user with this credintials'
    context['form'] = AuthenticationForm(request)
    return render(request, 'accounts/login.html', context)

@login_required
def logout_view(request):  
    if request.POST:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/logout.html', {})

@login_required
def profile_view(request):
    context = {
        'name': request.user.get_full_name(),
        'username': request.user.username,
        'email': request.user.email,
        'dob': request.user.date_of_birth,
        'submissions': request.user.submissions.all(),
        #'scores': request.user.scores.all,
    }
    return render(request, 'accounts/profile.html', context)