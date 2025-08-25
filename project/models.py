from django.db import models
from accounts.models import CustomUser
import uuid
from rest_framework.permissions import IsAuthenticated


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=5000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue = models.ForeignKey("Issue", on_delete=models.CASCADE, null=False, blank=False)
    time_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
    
    



class Contributor(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    STATUS_TODO = "To Do"
    

    [(STATUS_TODO.lower(), STATUS_TODO)]
    """ Faire ca pour inprogress, finished etc , tags / priority"""
     
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issues')
    time_created = models.DateTimeField(auto_now_add=True)


    STATUS_CHOICES = [("todo", "To do"), ("inprogress", "In Progress"), ("finished", "Finished")]
    TAG_CHOICES = [("bug", "BUG"), ("feature", "FEATURE"), ("task", "TASK")]
    PRIORITY_CHOICES = [("low", "LOW"), ("medium", "MEDIUM"), ("high", "HIGH")]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_TODO)
    tag = models.CharField(max_length=15, choices=TAG_CHOICES)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)

    attribution = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='attributed', null=True, blank=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='issues')

    def __str__(self):
        return self.name

class Project(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser,on_delete=models.PROTECT, related_name='projects')
    name = models.CharField(max_length=100)
    contributors = models.ManyToManyField(CustomUser, through='project.Contributor')
    description = models.TextField(max_length=5000)
    TYPE_CHOICES = [("backend", "Backend"), ("frontend", "Front-end"),("ios", "Ios"), ("android", "Android")]
    project_type = models.CharField(max_length=10, choices=TYPE_CHOICES)


    def __str__(self):
        return self.name





