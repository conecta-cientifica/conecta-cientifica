# Generated by Django 4.2.4 on 2023-10-07 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_projeto_requisitos_projeto_rename_profile_perfil_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResearchArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResearchProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('thesis', models.CharField(blank=True, max_length=100, null=True)),
                ('grade_area', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_area', models.CharField(blank=True, max_length=100, null=True)),
                ('specialty', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='', max_length=254)),
                ('tags', models.ManyToManyField(blank=True, to='accounts.tag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='linhas',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='userID',
        ),
        migrations.DeleteModel(
            name='Formacao_titulacao',
        ),
        migrations.DeleteModel(
            name='LinhaPesquisa',
        ),
        migrations.AddField(
            model_name='researchproject',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='research_projects', to='accounts.userprofile'),
        ),
        migrations.AddField(
            model_name='researcharea',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='research_areas', to='accounts.userprofile'),
        ),
        migrations.AddField(
            model_name='education',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='orientadorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='pesquisador_associado_projetc',
            field=models.ManyToManyField(related_name='projetos_pesquisados', through='accounts.ProjetoAssociacao', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='projetoassociacao',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]