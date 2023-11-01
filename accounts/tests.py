from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from . import views
from main import views 
from .forms import UserForm, LoginForm
from django.http import QueryDict



class YourAppTestCase(TestCase):

    def setUp(self):
        # Crie dados de exemplo para teste
        self.user_data = {
            'username': 'testuser',
            'password': 'Test12345',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)

    def tearDown(self):
        # Apague o usuário após cada teste
        self.user.delete()

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

    # def test_register_view_invalid(self):
    #     # Senha sem letra maiuscula
    #     user_data = {
    #         'username': 'joe',
    #         'password': 'semletramaiuscula',
    #         'password_confirmation': 'semletramaiuscula',
    #         'first_name': 'Joe',
    #         'last_name': 'Doe',
    #         'email': 'joe@example.com'
    #     }
    #     # Teste o registro de um usuário
    #     response = self.client.post(reverse('register'), data=user_data)
    #     self.assertEqual(response.status_code, 200)

    #     # Sem um campo
    #     user_data = {
    #         'password': 'semletramaiuscula',
    #         'password_confirmation': 'semletramaiuscula',
    #         'first_name': 'Joe',
    #         'last_name': 'Doe',
    #         'email': 'joe@example.com'
    #     }
    #     # Teste o registro de um usuário
    #     response = self.client.post(reverse('register'), data=user_data)
    #     self.assertEqual(response.status_code, 200)


    def test_login_view(self):
        # Teste o login de um usuário
        login_data = {
            'username': 'testuser',
            'password': 'Test12345'
        }
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 302)  # Verifique se a resposta é um redirecionamento
        self.assertRedirects(response, reverse(views.main_view))  # Verifique se o redirecionamento está correto

    # def test_login_view_invalid(self):
    #     # Teste o login de um usuário nao cadastrado no banco
    #     login_data = {
    #         'username': 'invalido',
    #         'password': 'Test12345'
    #     }
    #     response = self.client.post(reverse('login'), data=login_data)
    #     self.assertEqual(response.status_code, 200)

    #     # Faltando um campo
    #     login_data = {
    #         'password': 'Test12345'
    #     }
    #     response = self.client.post(reverse('login'), data=login_data)
    #     self.assertEqual(response.status_code, 200)

    def test_user_form(self):
        # Teste a validação do formulário de usuário
        form_data = QueryDict('username=joe&password=Test12345&password_confirmation=Test12345&first_name=Joe&last_name=Doe&email=joe@example.com')
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())  # Verifique se o formulário é válido

    def test_user_form_invalid(self):
        # Teste a validação do formulário faltando campo
        form_data = QueryDict('password=Test12345&password_confirmation=Test12345&first_name=Joe&last_name=Doe&email=joe@example.com')
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())  # Verifique se o formulário é inválido

        # Teste a validação do formulário com senha invalida
        form_data = QueryDict('username=joe&password=test12345&password_confirmation=test12345&first_name=Joe&last_name=Doe&email=joe@example.com')
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())  # Verifique se o formulário é inválido

        # Teste a validação do formulário com senha diferente da confirmação
        form_data = QueryDict('username=joe&password=Test12345&password_confirmation=Senhadiferente&first_name=Joe&last_name=Doe&email=joe@example.com')
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())  # Verifique se o formulário é válido        

    def test_login_form(self):
        # Testa a validação do formulário de login
        login_data = {
            'username': 'testuser',
            'password': 'Test12345'
        }
        form = LoginForm(data=login_data)
        self.assertTrue(form.is_valid())  # Verifique se o formulário de login é válido

    def test_login_form_invalid(self):
        # Testa a validação do formulário de login com dados inválidos
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'  # Senha incorreta
        }
        form = LoginForm(data=login_data)
        self.assertFalse(form.is_valid())  # Verifique se o formulário de login não é válido

        # Teste a validação do formulário de login com dados faltantes
        login_data = {
            'password': 'Correctgpassword' 
        }
        form = LoginForm(data=login_data)
        self.assertFalse(form.is_valid())  # Verifique se o formulário de login não é válido


    def test_user_detail_view(self):
      # Faça login
      self.client.login(username='testuser', password='Test12345')

      # Testar a visualização de detalhes do usuário existente
      response = self.client.get(reverse('user_detail', kwargs={'pk': self.user.pk}))
      #print(response.content)  # Imprima o conteúdo da resposta
      self.assertEqual(response.status_code, 200)  # Verifique se a página é acessível
      self.assertContains(response, self.user.username)  # Verifique se o nome de usuário está presente
      self.assertContains(response, self.user.email)  # Verifique se o email está presente

      # Testar a visualização de detalhes de um usuário que não existe
      non_existent_user_id = self.user.pk + 1
      response = self.client.get(reverse('user_detail', kwargs={'pk': non_existent_user_id}))
      #print(response.content)  # Imprima o conteúdo da resposta
      self.assertEqual(response.status_code, 404)  # Verifique se o usuário não existe

 
    def test_user_update_view(self):
      # Faça login
      self.client.login(username='testuser', password='Test12345')
      # Testar a atualização de detalhes do usuário existente
      update_data = {
          'username': 'updateduser',
          'email': 'updated@example.com',
          'first_name': 'Updated',
          'last_name': 'User',
          'password': 'NewPassword123',
          'password_confirmation': 'NewPassword123'
        } 
      response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), data=update_data)
      self.assertEqual(response.status_code, 302)  # Verifique se a atualização foi bem-sucedida

      updated_user = User.objects.get(pk=self.user.pk)
      self.assertEqual(updated_user.username, 'updateduser')  # Verifique se o nome de usuário foi atualizado
      self.assertEqual(updated_user.email, 'updated@example.com')  # Verifique se o email foi atualizado

      # Testar a atualização de detalhes de um usuário que não existe
      non_existent_user_id = self.user.pk + 1
      response = self.client.post(reverse('user_update', kwargs={'pk': non_existent_user_id}), data=update_data)
      self.assertEqual(response.status_code, 404)  # Verifique se o usuário não existe


    def test_user_delete_view(self):
      # Faça login
      self.client.login(username='testuser', password='Test12345')

    # Testar a exclusão de um usuário existente
      response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
      self.assertEqual(response.status_code, 302)  # Verifique se a exclusão foi bem-sucedida

      with self.assertRaises(User.DoesNotExist):
          User.objects.get(pk=self.user.pk)  # Verifique se o usuário não existe mais

      # Testar a exclusão de um usuário que não existe
      non_existent_user_id = self.user.pk + 1
      response = self.client.post(reverse('user_delete', kwargs={'pk': non_existent_user_id}))
      self.assertEqual(response.status_code, 404)  # Verifique se o usuário não existe




