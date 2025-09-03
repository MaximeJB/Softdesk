import uuid
from django.db import models
from accounts.models import CustomUser


class Comment(models.Model):
    """
    Model representing a comment made by a user on an issue

    Attributes : 
    id : UUID: Primary key
    description : text content
    author (ForeignKey) 
    issue (ForeignKey): related issue
    time_created (DateTimeField): Timestamp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=5000)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, blank=False)
    issue = models.ForeignKey(
        "Issue", on_delete=models.CASCADE, null=False, blank=False
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Contributor(models.Model):
    """
    Model representing a user contributing to ressources

    Attributes : 
    project (ForeignKey): related project
    user (ForeignKey): user 
    time_created : timestamp 

    Constraints : 
    unicity for project,user combination
    """
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"], name="unique_project_contributor"
            )
        ]


class Issue(models.Model):
    """
    Model representing an Issue in a project

    Attributes:
    name (Charfield): name
    description (Textfield): description
    author (ForeignKey): author
    time_created : timestamp
    status (Charfield): current status (todo, progress, finished)
    tag (Charfield): (bug, feature, task)
    priority (Charfield): (low, medium, high)
    attribution (ForeignKey): user assigned
    project (ForeignKey): related project
    """
    STATUS_TODO = "todo"
    [(STATUS_TODO.lower(), STATUS_TODO)]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    author = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=False, related_name="issues"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("todo", "To do"),
        ("inprogress", "In Progress"),
        ("finished", "Finished"),
    ]
    TAG_CHOICES = [("bug", "BUG"), ("feature", "FEATURE"), ("task", "TASK")]
    PRIORITY_CHOICES = [("low", "LOW"), ("medium", "MEDIUM"), ("high", "HIGH")]
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_TODO
    )
    tag = models.CharField(max_length=15, choices=TAG_CHOICES)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)

    attribution = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="attributed",
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="issues"
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Model representing a project.
    
    Attributes:
        time_created (DateTimeField): Creation timestamp.
        author (ForeignKey): Project creator.
        name (CharField): Project name.
        contributors (ManyToManyField): Users contributing to the project.
        description (TextField): Project description.
        project_type (CharField): Type (backend, frontend, ios, android).
    """
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects"
    )
    name = models.CharField(max_length=100)
    contributors = models.ManyToManyField(
        CustomUser, through="project.Contributor"
    )
    description = models.TextField(max_length=5000)
    TYPE_CHOICES = [
        ("backend", "Backend"),
        ("frontend", "Front-end"),
        ("ios", "Ios"),
        ("android", "Android"),
    ]
    project_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.author.username} -> {self.name}"
