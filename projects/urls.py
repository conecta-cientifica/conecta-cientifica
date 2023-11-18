from django.urls import path
from . import views

urlpatterns = [
    path('projects-feed/', views.projects_feed_view, name='projects-feed'),
    path('project/<int:project_id>/', views.project_page_view, name='project-page'),
    # path('project-page/', views.project_page_view, name='project-page'),
    path('create-project/', views.create_project, name='create-project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit-project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete-project'),
    path('subscribe-project/<int:project_id>/', views.subscribe_project, name='subscribe-project'),
    path('unsubscribe-project/<int:project_id>/', views.unsubscribe_project, name='unsubscribe-project'),
    path('subscription-requests/', views.subscription_requests, name='subscription-requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve-request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject-request'),
]
