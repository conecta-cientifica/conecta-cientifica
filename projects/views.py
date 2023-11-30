from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Project, SubscriptionRequest, SubscriptionHistory
from accounts.models import UserProfile
from .forms import ProjectForm, ProjectFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from itertools import groupby
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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
        'tags': project.tags.split(','),
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
            area = filter_form.cleaned_data.get('area')
            deadline = filter_form.cleaned_data.get('deadline')
            faculty = filter_form.cleaned_data.get('faculty')

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
            if area:
                query |= Q(area=area)
            if deadline:
                query |= Q(deadline=deadline)
            if faculty:
                query |= Q(faculty=faculty)
                
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


# SISTEMA DE RECOMENDAÇÕES
def recommend_projects(user_id, num_recommendations=5):
    # ID usuário
    user = get_user_model().objects.get(pk=user_id)

    try:
        # Verifica se UserProfile está criado para o usuário
        user_profile = UserProfile.objects.get(user=user)
        
        # Tags associadas ao usuário
        user_tags = user_profile.tags

        # Tags de todos os projetos no banco de dados
        projects = Project.objects.exclude(tags="")  # Exclui projetos sem tags

        # Filtra projetos que não tem tags em comum com o usuário e tem pelo menos uma tag
        relevant_projects = [project for project in projects if any(tag in user_tags.split(',') for tag in project.tags.split(','))]
   
        # Técnica TF-IDF para criar uma matriz de features a partir das tags dos projetos
        vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b', stop_words=None)
        projects_matrix = vectorizer.fit_transform([" ".join(project.tags.split(',')) for project in relevant_projects])

        # Técnica TF-IDF para criar uma matriz de features para as tags do usuário
        user_matrix = vectorizer.transform([" ".join(user_tags.split(','))])

        # Calcula a similaridade entre as tags do usuário e as tags dos projetos usando cosine similarity
        similarity_scores = cosine_similarity(user_matrix, projects_matrix)

        # Encontra o maior número de tags em comum
        max_common_tags = int(similarity_scores.max())

        # Define o valor mínimo de tags em comum necessário para um projeto ser recomendado
        min_common_tags = max(1, max_common_tags - 2)  # Define um mínimo de 1 tag em comum - ao alterar o valor de 1 a filtragem muda

        # Ordena os índices dos projetos com base na pontuação final, obtendo os mais similares
        recommended_projects_indices = similarity_scores.argsort(axis=1)[:, ::-1][:, :num_recommendations]

        # Filtra os projetos usando os índices recomendados e o número mínimo de tags em comum
        recommended_projects = [
            relevant_projects[i] for i in recommended_projects_indices[0]
            if len(set(user_tags.split(',')) & set(relevant_projects[i].tags.split(','))) >= min_common_tags
        ]
    except:
        recommended_projects = []
    return recommended_projects


@login_required(login_url='/login/')
def recommend_projects_view(request):
    context = {}
    
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        user_id = request.user.id  # ID do usuário
        
        # Chama a função de recomendação passando o ID do usuário
        recommended_projects = recommend_projects(user_id)
        if len(recommended_projects) == 0:
            messages.warning(request, 'Não há recomendações. Adicione mais informações na sua descrição!')
        
        # Obtem apenas os projetos recomendados do banco de dados
        recommended_project_ids = [project.id for project in recommended_projects]
        recommended_project_cards = Project.objects.filter(id__in=recommended_project_ids)
        
        context = {'recommended_projects': recommended_project_cards}

    return render(request, "recommended-projects.html", context)