# Generated by Django 3.2.23 on 2023-11-28 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20231128_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='pesquisador_associado_projetc',
            field=models.ManyToManyField(blank=True, related_name='projetos_pesquisados', through='accounts.ProjetoAssociacao', to='accounts.UserProfile'),
        ),
    ]
