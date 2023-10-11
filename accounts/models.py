from django.db import models
from django.contrib.auth.models import User

# class LinhaPesquisa(models.Model):
#     descricao = models.CharField(max_length=100, null=False, blank = False)

# class Perfil(models.Model):
#     userID = models.OneToOneField(User, on_delete = models.CASCADE)
#     linhas = models.ManyToManyField(LinhaPesquisa)

# class Formacao_titulacao(models.Model):
#     titulo = models.CharField(max_length=100)
#     curso = models.CharField(max_length=100, null=False, blank=False)
#     universidade = models.CharField(max_length=100, null=False, blank=False)
#     tese = models.CharField(max_length=200, blank=False, null=False)
#     grande_area = models.CharField(max_length=100)
#     area = models.CharField(max_length=100)
#     sub_area = models.CharField(max_length=100)
#     especialidade = models.CharField(max_length=100)
#     perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE) 

# Início cadastro usuário
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    tags = models.ManyToManyField('Tag', blank=True)

class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
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
    thesis = models.CharField(max_length=100, blank=True, null=True)
    grade_area = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    sub_area = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)

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

