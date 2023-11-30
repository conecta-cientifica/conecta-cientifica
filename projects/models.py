from django.db import models
from django.contrib.auth.models import User
import spacy


nlp = spacy.load('pt_core_news_sm')

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
        ('', 'Nenhuma'),  # Opção nula
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
        ('', 'Nenhum'),  # Opção nula
        ('Curto Prazo', 'Curto Prazo: até 6 meses'),
        ('Médio Prazo', 'Médio Prazo: 6 a 12 meses'),
        ('Longo Prazo', 'Longo Prazo: mais de 12 meses'),
    ]
    
    FACULTY_CHOICES = [(faculty.name, faculty.name) for faculty in Faculty.objects.all()]
    
    area = models.CharField(max_length=50, choices=AREAS_CHOICES, default='', null=False, blank=False)
    deadline = models.CharField(max_length=30, choices=DEADLINE_CHOICES, default='', null=False, blank=False)
    faculty = models.CharField(max_length=200, choices=FACULTY_CHOICES, default='', null=False, blank=False)
    
    def __str__(self):
        return self.title
    def set_requirements(self, requirements):
        # Processa as entradas separadas por vírgula e armazena como uma lista
        self.requirements = ','.join(requirements)
    def get_requirements(self):
        # Retorna a lista de requisitos
        return self.requirements.split(',')
    
    # TAGS
    tags = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Processa a descrição e os requisitos para extrair as tags
        text_to_process = f'{self.description} {self.requirements if hasattr(self, "requirements") else ""}'
        
        irrelevant = ["estudante", "professor", "pesquisa", "desenvolvimento", "avanço", 
                    "contribui", "estudo", "objetivo", "bacharelado", "mestrado", "doutorado", 
                    "bacharel", "mestre", "doutor", 
                    "estágio", "foco", 'análise', "universidade", "faculdade",
                      
                    "student", "professor", "research", "development", "advance",
                    "contribute", "study", "objective", "bachelor's degree", "master's degree", "doctorate",
                    "bachelor", "master", "doctor",
                    "internship", "focus", 'analysis', "university", "college"]
        
        if text_to_process:
            nlp = spacy.load('pt_core_news_sm')
            tokens = nlp(text_to_process)
            relevant_tags = [token.text for token in tokens if token.pos_ in ['NOUN'] and token.text.lower() not in irrelevant]

            # Verifica se há pelo menos uma palavra "relevante"
            if relevant_tags:
                num_tags_to_save = 25  # o número desejado de tags
                relevant_tags = relevant_tags + [''] * (num_tags_to_save - len(relevant_tags))
                relevant_tags = relevant_tags[:num_tags_to_save]
                tags_from_user = ','.join(relevant_tags)

                # Continue apenas se houver tags relevantes
                if tags_from_user:
                    self.tags = tags_from_user
                    super().save(*args, **kwargs)
            else:
                # Se não houver palavras relevantes, salva um conjunto vazio de tags
                self.tags = ''
                super().save(*args, **kwargs)

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