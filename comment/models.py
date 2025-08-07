from django.db import models
from users.models import CustomUser
from issue.models import Issue
import uuid


class Comment(models.Model):
    description = models.TextField(max_length=5000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lien = models.CharField(max_length=500)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField(auto_now_add=True)

