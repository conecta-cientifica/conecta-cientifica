from django.urls import path
from .views import main_view
from django.conf.urls.static import static
from conecta_cientifica import settings
urlpatterns = [
    path('', main_view, name='main')
] + static(settings.STATIC_ROOT)