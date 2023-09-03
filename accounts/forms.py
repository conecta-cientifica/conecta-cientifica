from django import forms
from django.contrib.auth.models import User
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile # TODO alterar "Profile" para o nome da classe corrta quando for criada no models.py
        
        # O usuário vai cadastrar todos os campos definidos na classe Profile
        # Exceto os campos selecionados no "exclude"
        # TODO necessário ajustes quando a classe Profile for criada
        fields = '__all__'
        exclude = ('usuario', ) # Nesse caso estou considerando que o usuário será escolhido automaticamente e não pelo usuário


class UserForm(forms.ModelForm): # Quais campos serão exibidos para o usuário - nem todos são necessários, alguns são apenas para admins, por exemplo.
    password = forms.CharField(
        required=False, # False porque quando o usuário está atualizando o perfil não é necessário atualizar a senha também
        widget=forms.PasswordInput(),
        label='Senha',
        # help_text = "A senha deve conter, no mínimo, 7 caracteres, incluindo pelo menos uma letra maiúscula e uma letra minúscula."
    )
    
    password_confirmation = forms.CharField(
        required=False, # False porque quando o usuário está atualizando o perfil não é necessário atualizar a senha também
        widget=forms.PasswordInput(),
        label='Confirmação Senha'
    )
    
    
    # Função personalizada (não existe no django, por isso é __init__) responsável por verificar o usuário:
    # se for None o usuário não está conectado, se for outro, aí é possível identificar qual é o usuário
    # A verificação deve ser feita no views.py. De lá vem a informação para essa função
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.usuario = usuario
         
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
                  'password', 'password_confirmation', 'email') # password está sendo deifnido no inicio da classe UserForm

    
    def validate_password(self, password_data, password_confirmation_data, validation_error_msgs):
        # Mensagens de erro
        error_msg_password_match = 'As senhas não são iguais.'
        error_msg_password_short = 'A senha precisa ter 7 caracteres ou mais.'
        error_msg_password_letters = 'A senha precisa ter letras maiúsculas E minúsculas.'
        
        # Validações
        if password_data != password_confirmation_data: # Campos senha e confirmação de senha não estão iguais
            validation_error_msgs['password'] = error_msg_password_match
            validation_error_msgs['password_confirmation_data'] = error_msg_password_match

        if len(password_data) < 7: # Senha possui menos de 7 caracteres
            validation_error_msgs['password'] = error_msg_password_short
            
        if not(any(char.isupper() for char in password_data) and any(char.islower() for char in password_data)): # Se a senha não possui letras maiúsculas E minúsculas
            validation_error_msgs['password'] = error_msg_password_letters
    
    
        
    def clean(self, *args, **kwargs): # Validar informações
        data = self.data # dados sem tratamento - vem do views.py
        cleaned = self.cleaned_data # dados tratados
        validation_error_msgs = {} # Erros
        
        # Coleta dos dados digitados pelo usuário no forms
        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_confirmation_data = cleaned.get('password_confirmation')
        
        # Busca no BD - verifica se determinado dado já foi cadastrado no banco de dados
        db_user = User.objects.filter(username=user_data).first() # Verifica se o usuário já está cadastrado no banco 
        db_email = User.objects.filter(email=email_data).first()
        
        # Mensagens
        error_msg_user_exists = 'Usuário já cadastrado.'
        error_msg_email_exists = 'E-mail já cadastrado.'
        error_msg_required_field = 'Campo obrigatório.'
        
        # Usuário está logado - atualização de dados
        if self.usuario:
            print('Usuário logado! ') # TODO debug
            if db_user: # Usuário no Forms existe no bd
                if user_data != db_user.username: # Usuário é diferente do usuário atual, significa que deseja-se atualizar esse campo - erro, pois o novo usuário digitado, como verificado no if acima, já existe no bd
                    validation_error_msgs['username'] = error_msg_user_exists

            if db_email: # E-mail no Forms existe no bd
                if email_data != db_email.email: # E-mail é diferente do e-mail atual, significa que deseja-se atualizar esse campo - erro, pois o novo e-mail digitado, como verificado no if acima, já existe no bd
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data: # Existe uma senha no forms
                self.validate_password(password_data, password_confirmation_data, validation_error_msgs)
        
        # Usuário NÃO está logado - cadastro
        else:
            print('Usuário deslogado!') # TODO debug
            
            if db_user: # Usuário já existe no bd 
                validation_error_msgs['username'] = error_msg_user_exists

            if db_email:
                validation_error_msgs['email'] = error_msg_email_exists
                
            if not user_data:
                validation_error_msgs['username'] = error_msg_required_field
                
            if not email_data:
                validation_error_msgs['email'] = error_msg_required_field

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password_confirmation_data:
                validation_error_msgs['password_confirmation_data'] = error_msg_required_field
                
            self.validate_password(password_data, password_confirmation_data, validation_error_msgs)
                
        if validation_error_msgs: # Exceção que ocorre se houver pelo menos uma mensgaem salva no dicionário de erros "validation_error_msgs"
            raise(forms.ValidationError(validation_error_msgs))
        
       