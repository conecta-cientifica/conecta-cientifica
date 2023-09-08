from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserForm#, ProfileForm # TODO: ProfileForm

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
            return redirect('página_de_sucesso')
    else:
        user_form = UserForm()
        # TODO: ProfileForm
        #profile_form = ProfileForm()
    return render(request, 'register.html', {'user_form': user_form, })#'profile_form': profile_form}) # TODO: ProfileForm
