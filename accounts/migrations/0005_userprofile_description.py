# Generated by Django 4.2.4 on 2023-11-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_remove_userprofile_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
    ]
