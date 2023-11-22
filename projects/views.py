from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, SubscriptionRequest, SubscriptionHistory
from .forms import ProjectForm, ProjectFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from itertools import groupby

@login_required(login_url='/login/')
def projects_feed_view(request):
    project_cards = Project.objects.all()  # Obtem todos os projetos do banco de dados
    return render(request, "projects-feed.html", {'project_cards': project_cards})

# Exibe o projeto escolhido pelo usuário no feed - na url fica o id do projeto
def project_page_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    subscription_request = project.subscriptionrequest_set.filter(user=request.user).first()

    # Dados referentes ao projeto que são enviados para o front
    context = {
        'project': project,
        'subscription_request': subscription_request,
        'is_creator': (project.creator == request.user) if request.user.is_authenticated else False,
        'subscription_status': subscription_request.get_approved_display() if subscription_request and hasattr(subscription_request, 'get_approved_display') and subscription_request.approved is not None else None,
        'creator_username': project.creator.username,
    }
    return render(request, 'project-page.html', context)

# Criação de projeto
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
        project_form = ProjectForm()

    return render(request, 'create_project.html', {
        'project_form': project_form
    })

# Edição de projeto
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

# Exclusão de projeto
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

# Inscrição em um projeto
@login_required(login_url='/login/')
def subscribe_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Verifica se o usuário é o criador do projeto
    if project.creator == request.user:
        messages.warning(request, 'Você não pode se inscrever no seu próprio projeto.')
    else:
        # Verifica se o usuário já está inscrito no projeto
        subscription_request_exists = SubscriptionRequest.objects.filter(
            project=project,
            user=request.user,
        ).exists()

        if subscription_request_exists:
            messages.warning(request, 'Você já enviou uma solicitação para este projeto.')
        else:
            # Cria a instância do SubscriptionRequest sem definir approved - será enviada uma solicitação de inscrição para o criador do projeto
            subscription_request = SubscriptionRequest.objects.create(
                project=project,
                user=request.user,
            )
            messages.success(request, 'Solicitação de inscrição enviada com sucesso.')

    # Após a inscrição, redireciona para a página do projeto
    return redirect('project-page', project_id=project_id)

# Visualizar inscrições em um projeto: apenas para criador do projeto
@login_required(login_url='/login/')
def subscription_requests(request):
    subscription_requests = SubscriptionRequest.objects.filter(project__creator=request.user)
    print(subscription_requests)

    # Se o formulário de aprovação/não aprovação for enviado
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        approval_status = request.POST.get('approval_status')  # 'approve' ou 'reject'

        # Atualiza o status da solicitação
        subscription_request = SubscriptionRequest.objects.get(id=request_id)
        subscription_request.approved = (approval_status == 'approve')
        subscription_request.save()

        # Adiciona ao histórico
        SubscriptionHistory.objects.create(
            project=subscription_request.project,
            user=subscription_request.user,
            approved=subscription_request.approved,
        )

    # Agrupa as solicitações por projeto
    grouped_requests = {}
    for project, requests in groupby(subscription_requests, key=lambda req: req.project):
        grouped_requests[project] = list(requests)

    return render(request, 'subscription-requests.html', {'grouped_requests': grouped_requests})

# Desinscrição em um projeto
@login_required(login_url='/login/')
def unsubscribe_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Verifica se o usuário está inscrito no projeto - status está "Em aberto" (para projetos em que a solicitação de inscrição já foi aprovada ou não aprovada não é possível cancelar a mesma)
    subscription_request_exists = SubscriptionRequest.objects.filter(
            project=project,
            user=request.user,
        ).exists()

    if subscription_request_exists:
        # Remove a inscrição do usuário no projeto
        SubscriptionRequest.objects.filter(
            project=project,
            user=request.user,
        ).delete()
        messages.success(request, 'Inscrição cancelada com sucesso.')
    else:
        messages.warning(request, 'Você não está inscrito neste projeto.')

    # Após o cancelamento, redireciona para a página do projeto
    return redirect('project-page', project_id=project_id)

# Filtros para o Feed
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
            approved_only = filter_form.cleaned_data.get('approved_only')
            rejected_only = filter_form.cleaned_data.get('rejected_only')

            query = Q()
        
            if title:
                query |= Q(title__icontains=title)
            if advisor:
                query |= Q(advisor__icontains=advisor)
            if description:
                query |= Q(description__icontains=description)
            if subscribed_only:
                query |= Q(subscriptionrequest__user=request.user, subscriptionrequest__approved=None)
            if created_by_user:
                query |= Q(creator=request.user)
            if approved_only:
                query |= Q(subscriptionrequest__user=request.user, subscriptionrequest__approved=True)
            if rejected_only:
                query |= Q(subscriptionrequest__user=request.user, subscriptionrequest__approved=False)

            # Aplica os filtros usando a lógica "OU"
            project_cards = project_cards.filter(query)
    else:
        filter_form = ProjectFilterForm()
        
    return render(request, "projects-feed.html", {'project_cards': project_cards, 'filter_form': filter_form})

# Aprovar inscrição
@login_required(login_url='/login/')
def approve_request(request, request_id):
    subscription_request = get_object_or_404(SubscriptionRequest, pk=request_id)
    subscription_request.approved = True
    subscription_request.save()
    messages.success(request, 'Solicitação aprovada com sucesso.')
    return redirect('subscription-requests')

# Não aprovar inscrição
@login_required(login_url='/login/')
def reject_request(request, request_id):
    subscription_request = get_object_or_404(SubscriptionRequest, pk=request_id)
    subscription_request.delete()
    messages.success(request, 'Solicitação rejeitada com sucesso.')
    return redirect('subscription-requests')
