from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LinhaPesquisa(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank = False)

class Profile(models.Model):
    userID = models.OneToOneField(User, on_delete = models.CASCADE)
    linhas = models.ManyToManyField(LinhaPesquisa)
    #projects = models.ManyToManyField(Projects)

class Formacao_titulacao(models.Model):
    titulo = models.CharField(max_length=100)
    curso = models.CharField(max_length=100, null=False, blank=False)
    universidade = models.CharField(max_length=100, null=False, blank=False)
    tese = models.CharField(max_length=200, blank=False, null=False)
    grande_area = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    sub_area = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE) 