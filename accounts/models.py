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
        # text_to_process = f'{self.description} {self.educations.first().course} {self.educations.first().degree}' # Usa os dados da descrição, curso e grau
        text_to_process = f'{self.description}' # Usa os dados da descrição
        
        irrelevant = ["estudante", "professor", "pesquisa", "desenvolvimento", "avanço", 
                    "contribui", "estudo", "objetivo", "bacharelado", "mestrado", "doutorado", 
                    "bacharel", "mestre", "doutor", 
                    "estágio", "foco", 'análise', "universidade", "faculdade",
                      
                    "student", "professor", "research", "development", "advance",
                    "contribute", "study", "objective", "bachelor's degree", "master's degree", "doctorate",
                    "bachelor", "master", "doctor",
                    "internship", "focus", 'analysis', "university", "college"]
        
        if text_to_process:
            tokens = nlp(text_to_process)
            relevant_tags = [token.text for token in tokens if token.pos_ in ['NOUN'] and token.text.lower() not in irrelevant]
        
            # Verifica se há pelo menos uma palavra "relevante"
            if relevant_tags:
                num_tags_to_save = 7  # o número desejado de tags
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
        
    
class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100, default='Graduação', blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
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
    requisitos = models.CharField(max_length=100, blank=True, null=True)

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    orientadorID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pesquisador_associado_projetc = models.ManyToManyField(
        UserProfile,
        related_name='projetos_pesquisados',
        through='ProjetoAssociacao', blank=True)
    requisito_orientado= models.ManyToManyField(Requisitos_Projeto)
    grande_area=models.CharField(max_length=100, blank=True, null=True)
    area=models.CharField(max_length=100, blank=True, null=True)
    sub_area=models.CharField(max_length=100, blank=True, null=True)
    bolsa=models.BooleanField(default=False, blank=True, null=True)

class ProjetoAssociacao(models.Model):
    perfil = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    is_orientador = models.BooleanField(default=False, blank=True, null=True)

