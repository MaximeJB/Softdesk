from django.db import models
from users.models import CustomUser

class Project(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='author')
    name = models.CharField(max_length=100)
    contributors = models.ManyToManyField(CustomUser, through='contributor.Contributor')
    description = models.TextField(max_length=5000)
    TYPE = [("backend", "Backend"), ("frontend", "Front-end"),("ios", "Ios"), ("android", "Android")]
    type = models.CharField(max_length=10, choices=TYPE)