# Generated by Django 4.2.4 on 2023-11-16 01:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_project_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='subscribers',
            field=models.ManyToManyField(blank=True, default=None, related_name='subscribed_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
