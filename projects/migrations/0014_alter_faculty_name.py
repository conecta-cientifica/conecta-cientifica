# Generated by Django 4.2.4 on 2023-11-22 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0013_faculty_remove_project_faculty_project_faculty"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faculty",
            name="name",
            field=models.CharField(default="", max_length=200, unique=True),
        ),
    ]
