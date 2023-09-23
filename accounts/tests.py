from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from . import views
from main import views 
# from .forms import UserForm, LoginForm


class YourAppTestCase(TestCase):

    def test_register_view(self):
        user_data = {
            'username': 'joe',
            'password': 'Test12345',
            'password_confirmation': 'Test12345',
            'first_name': 'Joe',
            'last_name': 'Doe',
            'email': 'joe@example.com'
        }
        # Teste o registro de um usuário
        response = self.client.post(reverse('register'), data=user_data)
        self.assertEqual(response.status_code, 302)  # Verifique se a resposta é um redirecionamento
        self.assertRedirects(response, reverse('login'))  # Verifique se o redirecionamento está correto

    def test_login_view(self):

        # Crie dados de exemplo para teste
        user_data = {
            'username': 'testuser',
            'password': 'Test12345',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }
        User.objects.create_user(**user_data)

        # Teste o login de um usuário
        login_data = {
            'username': 'testuser',
            'password': 'Test12345'
        }
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 302)  # Verifique se a resposta é um redirecionamento
        self.assertRedirects(response, reverse(views.main_view))  # Verifique se o redirecionamento está correto

    # def test_user_form(self):
    #     # Teste a validação do formulário de usuário
    #     form_data = {
    #         'username': 'testuser',
    #         'password': 'Test12345',
    #         'password_confirmation': 'Test12345',
    #         'first_name': 'Test',
    #         'last_name': 'User',
    #         'email': 'test@example.com'
    #     }
    #     form = UserForm(data=form_data)
    #     self.assertTrue(form.is_valid())  # Verifique se o formulário é válido

    # def test_user_form_invalid(self):
    #     # Teste a validação do formulário de usuário com dados inválidos
    #     form_data = {
    #         'username': 'testuser',
    #         'password': 'password',  # Senha inválida
    #         'password_confirmation': 'password_confirmation',  # Confirmação de senha inválida
    #         'first_name': 'Test',
    #         'last_name': 'User',
    #         'email': 'test@example.com'
    #     }
    #     form = UserForm(data=form_data)
    #     self.assertFalse(form.is_valid())  # Verifique se o formulário não é válido

    # def test_login_form(self):
    #     # Teste a validação do formulário de login
    #     login_data = {
    #         'username': 'testuser',
    #         'password': 'Test12345'
    #     }
    #     form = LoginForm(data=login_data)
    #     self.assertTrue(form.is_valid())  # Verifique se o formulário de login é válido

    # def test_login_form_invalid(self):
    #     # Teste a validação do formulário de login com dados inválidos
    #     login_data = {
    #         'username': 'testuser',
    #         'password': 'wrongpassword'  # Senha incorreta
    #     }
    #     form = LoginForm(data=login_data)
    #     self.assertFalse(form.is_valid())  # Verifique se o formulário de login não é válido
