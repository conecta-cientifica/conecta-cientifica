from django.shortcuts import render

def projects_feed_view(request):
    project_cards = [['Objeto 1', 'Objeto 2', 'Objeto 3'], ['Objeto 4', 'Objeto 5', 'Objeto 6']] #matriz (3 colunas) devera ser preenchida com dados do banco
    return render(request, "projects-feed.html", {'project_cards': project_cards})

def project_page_view(request):
    return render(request, "project-page.html")
