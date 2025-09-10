from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsAuthor, IsAuthorOfProject, IsCollab
from .models import Comment, Contributor, Issue, Project
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer,
)
from django.db import models

class ContributorViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing contributors

    Permission : 
        - authenticated
        - write : only project authors (admin)
    """
    queryset = Contributor.objects.select_related("user", "project")
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOfProject]

    def perform_create(self, serializer):
        project_pk = self.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_pk)
        serializer.save(project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """
    endpoint for managing comment

    Permissions:
        -Restricted to collaborators and comment authors.
    """
    queryset = Comment.objects.all().select_related('author', 'issue', 'issue__project')
    serializer_class = CommentSerializer
    permission_classes = [IsCollab, IsAuthor]

    def get_queryset(self):
        issue_pk = self.kwargs.get("issue_pk")
        if issue_pk is None:
            return super().get_queryset().order_by("time_created")
        return self.queryset.filter(issue_id=issue_pk).order_by("time_created")

    def perform_create(self, serializer):
        issue_id = self.kwargs.get("issue_pk")
        serializer.save(author=self.request.user, issue_id=issue_id)

    def get_object(self):
        """
        Surcharging to connect the project.object to the Comment instance, easier for the permission 
        without the N+1 request
        """
        obj = super().get_object()
        if hasattr(obj, "issue") and getattr(obj.issue, "project", None) is not None:
            obj.project = obj.issue.project
        return obj


class IssueViewSet(viewsets.ModelViewSet):
    """
    endpoint for managing issues in projects

    Permissions:
        -restricted to collaborators and issue authors.
    """
    queryset = Issue.objects.select_related("author", "project")
    serializer_class = IssueSerializer
    permission_classes = [IsCollab, IsAuthor]

    def get_queryset(self):
        """
        Filter issues by project 
        """
        qs = self.queryset
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return qs.filter(project_id=project_id)
        return qs

    def perform_create(self, serializer):
        """
        Save issue with current user as author and project from url
        """
        project_id = self.kwargs.get("project_pk")
        serializer.save(author=self.request.user, project_id=project_id)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    endpoint for managing projects

    Permissions:
        -Authenticated can create
        -Collaborators and authors can update/delete
    """
    queryset = Project.objects.select_related("author").prefetch_related("contributor_set__user")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsCollab, IsAuthor]

    def get_queryset(self):
        #change
        """
        Ne renvoyer que les projets où l'utilisateur est auteur ou contributeur.
        Cela empêche un utilisateur non-collaborateur de voir tous les projets.
        """
        user = self.request.user
        return self.queryset.filter(models.Q(author=user) | models.Q(contributor__user=user)).distinct()

    def perform_create(self, serializer):
        """
        Save project with current user as author
        Also add th author as a contributor"""
        project = serializer.save(author=self.request.user)
        Contributor.objects.get_or_create(
            project=project, user=self.request.user
        )
