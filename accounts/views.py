from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, LoginForm, UserProfileForm, EducationForm, ResearchAreaForm, ResearchProjectForm, LattesForm
from django.contrib import auth, messages
from main import views 
from django.contrib.auth.decorators import login_required
from .models import User, Education, UserProfile, ResearchArea, ResearchProject
from django.contrib.auth.decorators import login_required
from accounts.lattes.lattesadapter import LattesAdapter
from accounts.lattes.lattes import Lattes
from django.contrib.auth import logout

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid(): 
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            auth.login(request, user)
            messages.success(
                request, f'Registro realizado com sucesso.')
            return redirect('login')
        else:
            user_form = UserForm()
            messages.error(request, f'Erro de registro.')
    user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth.login(request, user)
            messages.success(
                request, f'Login realizado com sucesso.')
            return redirect(views.main_view)
        else:
            login_form = LoginForm()
            messages.error(request, f'Erro de login.')
    login_form = LoginForm()    
    return render(request, 'login.html', {'login_form': login_form})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect(views.main_view)

# @login_required(login_url='/login/')
# def user_profile_edit_view(request):
#     # Obtém o perfil do usuário atual ou cria um novo se não existir
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     # Obtém as informações de educação, área de pesquisa e projetos de pesquisa do usuário
#     education_instance = user_profile.educations.first()
#     research_area_instance = user_profile.research_areas.first()
#     research_project_instance = user_profile.research_projects.first() 

#     if request.method == 'POST':
#         user_profile_form = UserProfileForm(request.POST, instance=user_profile)
#         education_form = EducationForm(request.POST, instance=education_instance)
#         research_area_form = ResearchAreaForm(request.POST, instance=research_area_instance)
#         research_project_form = ResearchProjectForm(request.POST, instance=research_project_instance)
#         if 'user_profile_form' in request.POST:
#             # Verifica se todos os formulários são válidos e, em seguida, salva os dados no banco de dados

#             if user_profile_form.is_valid() and education_form.is_valid() and research_area_form.is_valid() and research_project_form.is_valid():
#                 user_profile_form.save()

#                 if education_instance is None:
#                     education_instance = Education(user_profile=user_profile)
#                 education_form = EducationForm(request.POST, instance=education_instance, initial={'user_profile': user_profile})
#                 if education_form.is_valid():
#                     education_form.save()

#                 if research_area_instance is None:
#                     research_area_instance = ResearchArea(user_profile=user_profile)
#                 research_area_form = ResearchAreaForm(request.POST, instance=research_area_instance, initial={'user_profile': user_profile})
#                 if research_area_form.is_valid():
#                     research_area_form.save()

#                 if research_project_instance is None:
#                     research_project_instance = ResearchProject(user_profile=user_profile)
#                 research_project_form = ResearchProjectForm(request.POST, instance=research_project_instance, initial={'user_profile': user_profile})
#                 if research_project_form.is_valid():
#                     research_project_form.save()

#         elif 'lattes_form' in request.POST:  
#             try:
#                 adapter = LattesAdapter(Lattes())
#                 lattes_id = str(request.POST['lattes_id'])
#                 lattes_profile = adapter.get_lattes_profile(lattes_id)
#                 #save profile
#                 for titulation in lattes_profile.titulations:
#                     education_instance = Education()
#                     education_instance.user_profile = user_profile
#                     education_instance.course = titulation.formation_degree
#                     education_instance.degree = titulation.formation_degree
#                     education_instance.university = titulation.university
#                     education_instance.start_date = None
#                     education_instance.end_date = None
#                     education_instance.save()
#                 for project in lattes_profile.projects:
#                     project_instance = ResearchProject()
#                     project_instance.user_profile = user_profile
#                     project_instance.title = project.project_name
#                     project_instance.description = project.project_description
#                     project_instance.save()
#                 for line in lattes_profile.lines:
#                     tag_instance, created = Tag.objects.get_or_create(name=line.line_description)
#                     if created:
#                         tag_instance.save()
#                     user_profile.tags = tag_instance
#                     user_profile.save()
#                 del adapter
#             except:
#                 pass
#                 #pop message of error in case of cnat get lattes_profile
                
#     else:
#         user = request.user
#         name = str(user.first_name) + ' ' + str(user.last_name)
#         user_profile_form = UserProfileForm(instance=user_profile, initial={
#             'name': name,
#             'email': user.email,
#         })

#         education_form = EducationForm(instance=education_instance)
#         research_area_form = ResearchAreaForm(instance=research_area_instance)
#         research_project_form = ResearchProjectForm(instance=research_project_instance)
#     lattes_form = LattesForm()

#     return render(request, 'user-profile-edit.html', {
#         'user_profile_form': user_profile_form,
#         'education_form': education_form,
#         'research_area_form': research_area_form,
#         'research_project_form': research_project_form,
#         'lattes_form': lattes_form
#     })

# @login_required(login_url='/login/')
# def user_detail(request, pk):
#     user = get_object_or_404(User, pk=pk)

#     # Obtém o perfil do usuário
#     user_profile = user.userprofile

#     # Obtém as informações relacionadas ao perfil
#     educations = user_profile.educations.all()
#     research_areas = user_profile.research_areas.all()
#     research_projects = user_profile.research_projects.all()

#     return render(request, 'user_detail.html', {
#         'user': user,
#         'user_profile': user_profile,
#         'educations': educations,
#         'research_areas': research_areas,
#         'research_projects': research_projects,
#     })

@login_required(login_url='/login/')
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Obtém o perfil do usuário
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    tags_list = user_profile.tags.split(',')
    return render(request, 'user_detail.html', {
        'user': user,
        'user_profile': user_profile,
        'tags_list': tags_list
    })

@login_required(login_url='/login/')
def user_update(request, pk):
    # Verificação para garantir que apenas o usuário autenticado pode atualizar sua própria conta
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        messages.error(request, 'Você não tem permissão para atualizar esta conta.')
        return redirect('user_detail', pk=user.pk) # Redireciona para a página do projeto
    
    # Obtém o perfil do usuário atual ou cria um novo se não existir
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # # Obtém as informações de educação, área de pesquisa e projetos de pesquisa do usuário
    # education_instance = user_profile.educations.first()
    # research_area_instance = user_profile.research_areas.first()
    # research_project_instance = user_profile.research_projects.first() 
    
    # print(f'user: {user_profile}')
    # print(f'educations: {education_instance}')
    # print(f'research_areas: {research_area_instance}')
    # print(f'research_projects: {research_project_instance}')

    
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        # education_form = EducationForm(request.POST, instance=education_instance)
        # research_area_form = ResearchAreaForm(request.POST, instance=research_area_instance)
        # research_project_form = ResearchProjectForm(request.POST, instance=research_project_instance)
        
        if 'user_profile_form' in request.POST:    
            # Verifica se todos os formulários são válidos e, em seguida, salva os dados no banco de dados
            if user_profile_form.is_valid():
                user_profile = user_profile_form.save(commit=False)
                print(f"Description from POST: {request.POST['description']}") 
                user_profile.description = request.POST['description']
                user_profile.save()
                messages.success(request, f'Atualização realizada com sucesso.')
                return redirect('user_detail', pk=pk)
                

                # if education_instance is None:
                #     education_instance = Education(user_profile=user_profile)
                # education_form = EducationForm(request.POST, instance=education_instance, initial={'user_profile': user_profile})
                # if education_form.is_valid():
                #     education_form.save()

                # if research_area_instance is None:
                #     research_area_instance = ResearchArea(user_profile=user_profile)
                # research_area_form = ResearchAreaForm(request.POST, instance=research_area_instance, initial={'user_profile': user_profile})
                # if research_area_form.is_valid():
                #     research_area_form.save()

                # if research_project_instance is None:
                #     research_project_instance = ResearchProject(user_profile=user_profile)
                # research_project_form = ResearchProjectForm(request.POST, instance=research_project_instance, initial={'user_profile': user_profile})
                # if research_project_form.is_valid():
                #     research_project_form.save()
            else:
                print(f"User Profile Form Errors: {user_profile_form.errors}")
                # print(f"Education Form Errors: {education_form.errors}")
                # print(f"Research Area Form Errors: {research_area_form.errors}")
                # print(f"Research Project Form Errors: {research_project_form.errors}")

        elif 'lattes_form' in request.POST:  
            try:
                adapter = LattesAdapter(Lattes())
                lattes_id = str(request.POST['lattes_id'])
                lattes_profile = adapter.get_lattes_profile(lattes_id)
                #save profile
                for titulation in lattes_profile.titulations:
                    education_instance = Education()
                    education_instance.user_profile = user_profile
                    education_instance.course = titulation.formation_degree
                    education_instance.degree = titulation.formation_degree
                    education_instance.university = titulation.university
                    education_instance.start_date = None
                    education_instance.end_date = None
                    education_instance.save()
                for project in lattes_profile.projects:
                    project_instance = ResearchProject()
                    project_instance.user_profile = user_profile
                    project_instance.title = project.project_name
                    project_instance.description = project.project_description
                    project_instance.save()
                # for line in lattes_profile.lines:
                #     tag_instance, created = Tag.objects.get_or_create(name=line.line_description)
                #     if created:
                #         tag_instance.save()
                #     user_profile.tags = tag_instance
                    user_profile.save()
                del adapter
            except:
                pass
                #pop message of error in case of cnat get lattes_profile
                
    else:
        user = request.user
        name = str(user.first_name) + ' ' + str(user.last_name)
        user_profile_form = UserProfileForm(instance=user_profile, initial={
            'name': name,
            'email': user.email,
            'description': user_profile.description,
        })

        # education_form = EducationForm(instance=education_instance)
        # research_area_form = ResearchAreaForm(instance=research_area_instance)
        # research_project_form = ResearchProjectForm(instance=research_project_instance)
    # lattes_form = LattesForm()

    return render(request, 'user_update.html', {
        'user_profile_form': user_profile_form,
        # 'education_form': education_form,
        # 'research_area_form': research_area_form,
        # 'research_project_form': research_project_form,
        # 'lattes_form': lattes_form,
    })



def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Verificação para garantir que apenas o usuário autenticado pode excluir sua própria conta
    if user != request.user:
        messages.error(request, 'Você não tem permissão para excluir esta conta.')
        return redirect('user_detail', pk=user.pk) # Redireciona para a página do projeto
    
    if request.method == 'POST':
        user.delete()
        return redirect('login')
    return render(request, 'user_confirm_delete.html', {'user': user})