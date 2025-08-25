from django.shortcuts import render
from rest_framework import viewsets
from .models import Contributor
from .models import Comment
from .models import Issue
from .models import Project
from .serializers import ContributorSerializer
from .serializers import CommentSerializer
from .serializers import IssueSerializer
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from project.permissions import IsAuthor, IsAuthorOfProject
from project.permissions import IsCollab


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOfProject]
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCollab, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    