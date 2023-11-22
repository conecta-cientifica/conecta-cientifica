from django.db import models
from django.contrib.auth.models import User

# Início cadastro usuário
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    tags = models.ManyToManyField('Tag', blank=True)
    isTeacher = models.BooleanField(default=False)
    
class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100, default='Graduação')
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class ResearchArea(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='research_areas')
    name = models.CharField(max_length=100, blank=True, null=True)

class ResearchProject(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='research_projects')
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
# Fim cadastro usuário

class Requisitos_Projeto(models.Model):
    requisitos = models.CharField(max_length=100)

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    orientadorID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pesquisador_associado_projetc = models.ManyToManyField(
        UserProfile,
        related_name='projetos_pesquisados',
        through='ProjetoAssociacao')
    requisito_orientado= models.ManyToManyField(Requisitos_Projeto)
    grande_area=models.CharField(max_length=100, blank=True, null=True)
    area=models.CharField(max_length=100, blank=True, null=True)
    sub_area=models.CharField(max_length=100, blank=True, null=True)
    bolsa=models.BooleanField(default=False)

class ProjetoAssociacao(models.Model):
    perfil = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    is_orientador = models.BooleanField(default=False)

