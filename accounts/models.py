from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LinhaPesquisa(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank = False)

class Perfil(models.Model):
    userID = models.OneToOneField(User, on_delete = models.CASCADE)
    linhas = models.ManyToManyField(LinhaPesquisa)

class Formacao_titulacao(models.Model):
    titulo = models.CharField(max_length=100)
    curso = models.CharField(max_length=100, null=False, blank=False)
    universidade = models.CharField(max_length=100, null=False, blank=False)
    tese = models.CharField(max_length=200, blank=False, null=False)
    grande_area = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    sub_area = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE) 

class Requisitos_Projeto(models.Model):
    requisitos = models.CharField(max_length=100)

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    orientadorID = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    pesquisador_associado_projetc = models.ManyToManyField(
        Perfil,
        related_name='projetos_pesquisados',
        through='ProjetoAssociacao')
    requisito_orientado= models.ManyToManyField(Requisitos_Projeto)
    grande_area=models.CharField(max_length=100, blank=True, null=True)
    area=models.CharField(max_length=100, blank=True, null=True)
    sub_area=models.CharField(max_length=100, blank=True, null=True)
    bolsa=models.BooleanField(default=False)

class ProjetoAssociacao(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    is_orientador = models.BooleanField(default=False)

