from django.db import models
from users.models import CustomUser
from project.models import Project

# Create your models here.
class Contributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)