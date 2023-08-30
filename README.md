# conecta-cientifica
Este projeto faz parte dos requisitos para a conclusão da disciplina Engenharia de Software do ICT - UNIFESP São José dos Campos.


Criar um ambiente virtual:
python -m venv venv

Ativar a venv:
Linux: source venv/bin/activate  
Windows: venv\Scripts\activate


Instalar as dependências (bibliotecas e pacotes necessários para o projeto):
pip install -r requirements.txt


Configuração do banco de dados:
python manage.py migrate


Crie um superusuário (opcional):
python manage.py createsuperuser


Execute o servidor de desenvolvimento:
python manage.py runserver


Outros comandos:
Criar um app:
python manage.py startapp nome_do_app

Verificar se há algum erro
python manage.py check

Aplicar as migrações* do banco de dados. (*Migrações são uma forma de você manter o esquema do banco de dados sincronizado com o estado atual dos seus modelos (tabelas) no código.)
python manage.py migrate 

