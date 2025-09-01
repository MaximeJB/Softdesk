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


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing contributors

    Permission : 
        - authenticated
        - write : only project authors (admin)
    """
    queryset = Contributor.objects.all()
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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCollab, IsAuthor]

    def perform_create(self, serializer):
        issue_id = self.kwargs.get("issue_pk")
        serializer.save(author=self.request.user, issue_id=issue_id)


class IssueViewSet(viewsets.ModelViewSet):
    """
    endpoint for managing issues in projects

    Permissions:
        -restricted to collaborators and issue authors.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsCollab, IsAuthor]

    def get_queryset(self):
        """
        Filter issues by project 
        """
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return Issue.objects.filter(project_id=project_id)
        return Issue.objects.all()

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
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsCollab, IsAuthor]

    def perform_create(self, serializer):
        """
        Save project with current user as author
        Also add th author as a contributor"""
        project = serializer.save(author=self.request.user)
        Contributor.objects.get_or_create(
            project=project, user=self.request.user
        )
