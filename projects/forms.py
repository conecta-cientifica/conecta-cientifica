from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'advisor', 'description', 'requirements']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'advisor': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'requirements': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProjectFilterForm(forms.Form):
    title = forms.CharField(label='Título do Projeto', required=False)
    description = forms.CharField(label='Descrição', required=False)
    advisor = forms.CharField(label='Professor', required=False)
    subscribed_only = forms.BooleanField(label='Estou inscrito', required=False)
    created_by_user = forms.BooleanField(label='Criado por mim', required=False)

    # Adicionando um campo de reset para limpar os filtros
    reset_filters = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=True)
    