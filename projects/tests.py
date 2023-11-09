from django.test import TestCase
from django.urls import reverse
from .models import Project
from .forms import ProjectForm

class ProjectModelTestCase(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(
            title="Test Project",
            advisor="Test Advisor",
            description="Test Description",
            requirements="Test Requirements"
        )
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.advisor, "Test Advisor")
        self.assertEqual(project.description, "Test Description")
        self.assertEqual(project.requirements, "Test Requirements")
        print('test_project_creation')

class ProjectFormTestCase(TestCase):
    def test_valid_project_form(self):
        form_data = {
            'title': 'Test Project',
            'advisor': 'Test Advisor',
            'description': 'Test Description',
            'requirements': 'Test Requirements',
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
        print('test_valid_project_form')

class ProjectViewsTestCase(TestCase):
    def test_projects_feed_view(self):
        response = self.client.get(reverse('projects-feed'))
        self.assertEqual(response.status_code, 200)
        print('test_projects_feed_view')

    def test_project_page_view(self):
        response = self.client.get(reverse('project-page'))
        self.assertEqual(response.status_code, 200)
        print('test_project_page_view')

class ProjectDeleteTestCase(TestCase):
    def test_project_delete_view(self):
        project = Project.objects.create(
            title="Test Project",
            advisor="Test Advisor",
            description="Test Description",
            requirements="Test Requirements"
        )
        response = self.client.post(reverse('delete-project', args=[project.id]))
        self.assertEqual(response.status_code, 302)  # Redirecionamento após exclusão
        self.assertFalse(Project.objects.filter(id=project.id).exists())
        print('test_project_delete_view')
