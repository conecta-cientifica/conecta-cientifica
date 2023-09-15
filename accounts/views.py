from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm#, ProfileForm # TODO: ProfileForm
from django.http import HttpResponse
from django.contrib import auth
import pdb
from main import views 
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django.conf import settings
from django.http import HttpResponseRedirect

CLIENT_ID = settings.CLIENT_ID # Usado na autenticação do google


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        #profile_form = ProfileForm(request.POST)
        if user_form.is_valid(): #and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            # TODO: ProfileForm
            # profile = profile_form.save(commit=False)
            # profile.usuario = user
            # profile.save()
            login(request, user)
            return(redirect('login'))
    else:
        user_form = UserForm()
        # TODO: ProfileForm
        #profile_form = ProfileForm()
    return render(request, 'register.html', {'user_form': user_form, })#'profile_form': profile_form}) # TODO: ProfileForm

def login(request):
    #pdb.set_trace()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form['username'].value()
            password = login_form['password'].value()
            user = auth.authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                auth.login(request, user)
                return(redirect(views.main_view))
            else:
                return(redirect('login'))
    else:
        login_form = LoginForm()
        return(render(request, 'login.html',  {'login_form': login_form, 'CLIENT_ID': CLIENT_ID}))