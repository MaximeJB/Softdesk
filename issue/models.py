from django.db import models
from users.models import CustomUser
from project.models import Project



class Issue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='auteur')
    time_created = models.DateTimeField(auto_now_add=True)


    STATUS = [("todo", "To do"), ("in progress", "In Progress"), ("finished", "Finished")]
    BALISE = [("bug", "BUG"), ("feature", "FEATURE"), ("task", "TASK")]
    PRIORITY = [("low", "LOW"), ("medium", "MEDIUM"), ("high", "HIGH")]
    status = models.CharField(max_length=15, choices=STATUS, default="To do")
    balise = models.CharField(max_length=15, choices=BALISE)
    priority = models.CharField(max_length=15, choices=PRIORITY)

    attribution = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attributions', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')