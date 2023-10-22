from django.urls import path, include
from accounts import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('user-profile/', views.user_profile_view, name='user-profile'),
    path('user-profile-edit/', views.user_profile_edit_view, name='user-profile-edit'),
    path('accounts/', include('allauth.urls')),
]