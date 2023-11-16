from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    advisor = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_projects', default=None, blank=True)

    def __str__(self):
        return self.title
