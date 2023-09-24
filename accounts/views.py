from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm
from django.contrib import auth
import pdb
from main import views 
from django.conf import settings


def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid(): 
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            auth.login(request, user)
            return(redirect('login'))
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth.login(request, user)
            return redirect(views.main_view)
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form, 'CLIENT_ID': settings.CLIENT_ID})

def user_profile_view(request):
    return render(request, "user-profile.html")
