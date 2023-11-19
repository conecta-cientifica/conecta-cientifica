"""
URL configuration for conecta_cientifica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import urls as main_app_urls
from accounts import urls as accounts_app_urls
from projects import urls as projects_app_urls
from django.conf.urls.static import static
from conecta_cientifica import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(accounts_app_urls)),
    path('', include(projects_app_urls)),
    path('', include(main_app_urls))
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)