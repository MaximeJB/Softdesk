from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from project.permissions import IsAuthor, IsAuthorOfProject, IsCollab
from .models import Comment, Contributor, Issue, Project
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer,
)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOfProject]

    def perform_create(self, serializer):
        project_pk = self.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_pk)
        serializer.save(project=project)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCollab, IsAuthor]

    def perform_create(self, serializer):
        issue_id = self.kwargs.get("issue_pk")
        serializer.save(author=self.request.user, issue_id=issue_id)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsCollab, IsAuthor]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return Issue.objects.filter(project_id=project_id)
        return Issue.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        serializer.save(author=self.request.user, project_id=project_id)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCollab, IsAuthor]

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.get_or_create(
            project=project, user=self.request.user
        )
