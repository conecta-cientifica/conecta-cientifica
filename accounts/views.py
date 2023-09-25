from django.contrib.auth import login
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm
from django.contrib import auth
import pdb
from main import views 
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid(): 
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            auth.login(request, user)
            return redirect('login')
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




@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'user_update.html', {'form': form})




def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('login')
    return render(request, 'user_confirm_delete.html', {'user': user})