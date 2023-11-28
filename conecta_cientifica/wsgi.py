"""
WSGI config for conecta_cientifica project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

with open('requirements.txt', 'r') as arquivo:
    # Lê todo o conteúdo do arquivo e o imprime
    conteudo = arquivo.read()
    print(conteudo)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conecta_cientifica.settings')

application = get_wsgi_application()
