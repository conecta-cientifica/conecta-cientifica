from django.urls import path
from .views import main_view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', main_view, name='main')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)