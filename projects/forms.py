from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    requirements = forms.CharField(label='Requisitos do Projeto (separados por vírgula)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Project
        fields = ['title', 'advisor', 'description', 'requirements']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'advisor': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título do Projeto',
            'advisor': 'Professor Orientador',
            'description': 'Descrição do projeto',
        }

class ProjectFilterForm(forms.Form):
    title = forms.CharField(label='Título do Projeto', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Descrição', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    advisor = forms.CharField(label='Professor', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    created_by_user = forms.BooleanField(label='Criados por mim', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    subscribed_only = forms.BooleanField(label='Inscrições solicitadas', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    approved_only = forms.BooleanField(label='Inscrições aprovadas', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    rejected_only = forms.BooleanField(label='Inscrições não aprovadas', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    # Adicionando um campo de reset para limpar os filtros
    reset_filters = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=True)