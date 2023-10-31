from django.urls import path
from projects import views

urlpatterns = [
    path('projects-feed/', views.projects_feed_view, name='projects-feed'),
    path('project-page/', views.project_page_view, name='project-page')
]