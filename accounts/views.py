from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm, UserProfileForm, EducationForm, ResearchAreaForm, ResearchProjectForm, TagForm
from django.contrib import auth
import pdb
from main import views 
from .models import Education, UserProfile, ResearchArea, ResearchProject
from django.contrib.auth.decorators import login_required


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
    return render(request, 'login.html', {'login_form': login_form})

def user_profile_view(request):
    return render(request, "user-profile.html")

@login_required(login_url='/login/')
def user_profile_edit_view(request):
    # Obtém o perfil do usuário atual ou cria um novo se não existir
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Obtém as informações de educação, área de pesquisa e projetos de pesquisa do usuário
    education_instance = user_profile.educations.first()
    research_area_instance = user_profile.research_areas.first()
    research_project_instance = user_profile.research_projects.first()

    if request.method == 'POST':
        # Verifica se todos os formulários são válidos e, em seguida, salva os dados no banco de dados
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        education_form = EducationForm(request.POST, instance=education_instance)
        research_area_form = ResearchAreaForm(request.POST, instance=research_area_instance)
        research_project_form = ResearchProjectForm(request.POST, instance=research_project_instance)

        if user_profile_form.is_valid() and education_form.is_valid() and research_area_form.is_valid() and research_project_form.is_valid():
            user_profile_form.save()
            
            if education_instance is None:
                education_instance = Education(user_profile=user_profile)
            education_form = EducationForm(request.POST, instance=education_instance, initial={'user_profile': user_profile})
            if education_form.is_valid():
                education_form.save()

            if research_area_instance is None:
                research_area_instance = ResearchArea(user_profile=user_profile)
            research_area_form = ResearchAreaForm(request.POST, instance=research_area_instance, initial={'user_profile': user_profile})
            if research_area_form.is_valid():
                research_area_form.save()

            if research_project_instance is None:
                research_project_instance = ResearchProject(user_profile=user_profile)
            research_project_form = ResearchProjectForm(request.POST, instance=research_project_instance, initial={'user_profile': user_profile})
            if research_project_form.is_valid():
                research_project_form.save()
            
    else:
        user = request.user
        user_profile_form = UserProfileForm(instance=user_profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

        education_form = EducationForm(instance=education_instance)
        research_area_form = ResearchAreaForm(instance=research_area_instance)
        research_project_form = ResearchProjectForm(instance=research_project_instance)

    return render(request, 'user-profile-edit.html', {
        'user_profile_form': user_profile_form,
        'education_form': education_form,
        'research_area_form': research_area_form,
        'research_project_form': research_project_form,
    })
    