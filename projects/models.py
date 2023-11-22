from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    name = models.CharField(max_length=200, default='', null=False, blank=False, unique=True)
    sigla = models.CharField(max_length=20, default='', null=False, blank=False, unique=False)
    def __str__(self):
        return(self.name)

class Project(models.Model):
    title = models.CharField(max_length=200)
    advisor = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    requirements = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_projects', default=None, blank=True)
    requires_approval = models.BooleanField(default=False)
    
    AREAS_CHOICES = [
        ('', ''),  # Opção nula
        ('Ciências Ambientais', 'Ciências Ambientais (Ecologia, Geologia, etc)'),
        ('Ciências da Saúde', 'Ciências da Saúde (Medicina, Biomedicina, etc)'),
        ('Ciências Exatas', 'Ciências Exatas (Matemática, Estatística, etc)'),
        ('Ciências Naturais', 'Ciências Naturais (Biologia, Química, Física, etc)'),
        ('Ciências Sociais', 'Ciências Sociais (Psicologia, Sociologia, etc)'),
        ('Engenharia', 'Engenharia (Elétrica, Mecânica, de Software, etc)'),
        ('Humanidades', 'Humanidades (História, Literatura, etc)'),
        ('Tecnologia da Informação', 'Tecnologia da Informação (IA, Segurança da Informação, etc)'),
    ]

    DEADLINE_CHOICES = [
        ('', ''),  # Opção nula
        ('Curto Prazo', 'Curto Prazo: até 6 meses'),
        ('Médio Prazo', 'Médio Prazo: 6 a 12 meses'),
        ('Longo Prazo', 'Longo Prazo: mais de 12 meses'),
    ]
    
    area = models.CharField(max_length=50, choices=AREAS_CHOICES, default='', null=False, blank=False)
    deadline = models.CharField(max_length=30, choices=DEADLINE_CHOICES, default='', null=False, blank=False)
    faculty = models.ManyToManyField(Faculty)
    
    def __str__(self):
        return self.title
    def set_requirements(self, requirements):
        # Processa as entradas separadas por vírgula e armazena como uma lista
        self.requirements = ','.join(requirements)
    def get_requirements(self):
        # Retorna a lista de requisitos
        return self.requirements.split(',')

class SubscriptionRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True, blank=True)

class SubscriptionHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.project.title} - {self.approved}'