from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm, ProjectFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

@login_required(login_url='/login/')
def projects_feed_view(request):
    project_cards = Project.objects.all()  # Obtem todos os projetos do banco de dados
    return render(request, "projects-feed.html", {'project_cards': project_cards})


# Exibe o projeto escolhido pelo usuário no feed - na url fica o id do projeto
@login_required(login_url='/login/')
def project_page_view(request, project_id):
    try:
        project = get_object_or_404(Project, pk=project_id)
        
        # Verifica se o usuário logado é o criador do projeto
        is_creator = project.creator == request.user if project.creator else False
        
        return render(request, "project-page.html", {'project': project, 'is_creator': is_creator})
    except Http404: # Se o projeto não for encontrado, redireciona para o feed de projetos
        return redirect('projects-feed')

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
                return redirect('project-page', project_id=project_id) # redireciona para a página do projeto
        else:
            form = ProjectForm(instance=project)
        return render(request, 'edit_project.html', {'form': form, 'project': project})
    else:
        messages.error(request, 'Você não tem permissão para editar este projeto.')
        return redirect('project-page', project_id=project_id) # redireciona para a página do projeto

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
    
@login_required(login_url='/login/')
def subscribe_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Verifica se o usuário é o criador do projeto
    if project.creator == request.user:
        messages.warning(request, 'Você não pode se inscrever no seu próprio projeto.')
    else:
        # Verifica se o usuário já está inscrito no projeto
        if request.user in project.subscribers.all():
            messages.warning(request, 'Você já está inscrito neste projeto.')
        else:
            # Adiciona o usuário à lista de inscritos
            project.subscribers.add(request.user)
            messages.success(request, 'Inscrição realizada com sucesso.')

    # Após a inscrição, redireciona para a página do projeto
    return redirect('project-page', project_id=project_id)

@login_required(login_url='/login/')
def unsubscribe_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Verifica se o usuário está inscrito no projeto
    if request.user in project.subscribers.all():
        # Remove o usuário da lista de inscritos
        project.subscribers.remove(request.user)
        messages.success(request, 'Inscrição cancelada com sucesso.')
    else:
        messages.warning(request, 'Você não está inscrito neste projeto.')

    # Após o cancelamento, redireciona para a página do projeto
    return redirect('project-page', project_id=project_id)


@login_required(login_url='/login/')
def projects_feed_view(request):
    project_cards = Project.objects.all()

    # Se o formulário de filtro for enviado
    if request.method == 'GET':
        filter_form = ProjectFilterForm(request.GET)
        if filter_form.is_valid():
            title = filter_form.cleaned_data.get('title')
            advisor = filter_form.cleaned_data.get('advisor')
            description = filter_form.cleaned_data.get('description')
            subscribed_only = filter_form.cleaned_data.get('subscribed_only')
            created_by_user = filter_form.cleaned_data.get('created_by_user')

            # Aplica os filtros ao QuerySet
            if title:
                project_cards = project_cards.filter(title__icontains=title)
            if advisor:
                project_cards = project_cards.filter(advisor__icontains=advisor)
            if description:
                project_cards = project_cards.filter(description__icontains=description)
            if subscribed_only:
                project_cards = project_cards.filter(subscribers=request.user)
            if created_by_user:
                project_cards = project_cards.filter(creator=request.user)
    else:
        filter_form = ProjectFilterForm()
        
    return render(request, "projects-feed.html", {'project_cards': project_cards, 'filter_form': filter_form})

