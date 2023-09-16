from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Usuário'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha'
    )


class UserForm(forms.ModelForm): 
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        help_text="A senha deve conter, no mínimo, 7 caracteres, incluindo pelo menos uma letra maiúscula e uma letra minúscula.",
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z]).{7,}$', # Verifica se a senha está no padrão solicitado
                message="A senha não está no padrão."
            )
        ]
    )
    
    password_confirmation = forms.CharField(
        required=True, #True para registro 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmação Senha'
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nome'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Sobrenome'
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Usuário',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9@.+_/-]*$',
                message="O nome de usuário deve conter apenas letras, números e os caracteres @, +, -, _, ."
            )
        ]        
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='E-mail'
    )
    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
                  'password', 'password_confirmation', 'email') 
    
        
    def clean(self):
        cleaned = super().clean()
        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_confirmation_data = cleaned.get('password_confirmation')
        
        db_user = User.objects.filter(username=user_data).first()
        db_email = User.objects.filter(email=email_data).first()
        
        error_msgs = {}
        
        if db_user:
            if self.instance != db_user: 
                error_msgs['username'] = 'Usuário já cadastrado.'
        
        if db_email:
            if self.instance != db_user: 
                error_msgs['email'] = 'E-mail já cadastrado.'
        
        if password_data != password_confirmation_data:
            error_msgs['password_confirmation'] = 'As senhas não são iguais.'
        
        if error_msgs:
            raise forms.ValidationError(error_msgs)
        
        return cleaned
    