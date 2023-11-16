from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/login/')
def projects_feed_view(request):
    project_cards = Project.objects.all()  # Obtenha todos os projetos do banco de dados
    return render(request, "projects-feed.html", {'project_cards': project_cards})


# Exibe o projeto escolhido pelo usuário no feed - na url fica o id do projeto
@login_required(login_url='/login/')
def project_page_view(request, project_id):
    print(f'PROJECT ID: {project_id}')  # Isso verificará se o ID do projeto está correto
    project = get_object_or_404(Project, pk=project_id)
    
    print(f'Project Title: {project.title}')  # Isso imprimirá o título do projeto
    print(f'Advisor: {project.advisor}')  # Isso imprimirá o professor orientador
    print(f'Description: {project.description}')  # Isso imprimirá a descrição do projeto

    # print('Requirements:')  # Isso imprimirá os requisitos do projeto
    print(project.requirements)
    
    # Verifica se o usuário logado é o criador do projeto
    is_creator = project.creator == request.user if project.creator else False
    
    return render(request, "project-page.html", {'project': project, 'is_creator': is_creator})

@login_required(login_url='/login/')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user  # Salva o user que criou o projeto
            project.save()
            return redirect('projects-feed')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required(login_url='/login/')
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects-feed')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required(login_url='/login/')
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects-feed')
    return render(request, 'delete_project.html', {'project': project})

@login_required(login_url='/login/')
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Verifica se o usuário logado é o criador do projeto
    if project.creator == request.user:
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                messages.success(request, 'Projeto editado com sucesso.')
                return redirect('projects-feed')
        else:
            form = ProjectForm(instance=project)
        return render(request, 'edit_project.html', {'form': form, 'project': project})
    else:
        messages.error(request, 'Você não tem permissão para editar este projeto.')
        return redirect('projects-feed')

@login_required(login_url='/login/')
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Verifica se o usuário logado é o criador do projeto
    if project.creator == request.user:
        if request.method == 'POST':
            project.delete()
            messages.success(request, 'Projeto excluído com sucesso.')
            return redirect('projects-feed')
        return render(request, 'delete_project.html', {'project': project})
    else:
        messages.error(request, 'Você não tem permissão para excluir este projeto.')
        return redirect('projects-feed')