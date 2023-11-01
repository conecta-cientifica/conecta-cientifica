from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    advisor = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()

    def __str__(self):
        return self.title
