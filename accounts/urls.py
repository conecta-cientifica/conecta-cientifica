from django.urls import path, include
from accounts import views
from django.conf.urls.static import static
from conecta_cientifica import settings

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('user/<int:pk>/update/', views.user_update, name='user_update'),
    path('user/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('user-profile/', views.user_profile_view, name='user-profile'),
    path('user-profile-edit/', views.user_profile_edit_view, name='user-profile-edit'),
    path('accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

