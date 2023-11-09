from django.urls import path
from . import views

urlpatterns = [
    path('projects-feed/', views.projects_feed_view, name='projects-feed'),
    path('project/<int:project_id>/', views.project_page_view, name='project-page'),
    # path('project-page/', views.project_page_view, name='project-page'),
    path('create-project/', views.create_project, name='create-project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit-project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete-project'),
]
