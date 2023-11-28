from django.db import models
from django.contrib.auth.models import User
import spacy

nlp = spacy.load('pt_core_news_sm')

# Início cadastro usuário   
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    description = models.TextField(default='', blank=True, null=True)
    isTeacher = models.BooleanField(default=False)
    
    # TAGS
    tags = models.TextField(blank=True)
        
    def save(self, *args, **kwargs):
        # Processa as tags baseadas na descrição do usuário
        text_to_process = f'{self.description} {self.educations.first().course} {self.educations.first().degree}' # Usa os dados da descrição, curso e grau
        print(text_to_process)
        if text_to_process:
            tags_from_user = ','.join([token.text for token in nlp(text_to_process) if token.pos_ in ['NOUN', 'ADJ']])
            self.tags = tags_from_user
        super().save(*args, **kwargs)

        
    
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

