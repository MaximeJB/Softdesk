from rest_framework.permissions import SAFE_METHODS, BasePermission
from project.models             import Contributor, Project


class IsAuthor(BasePermission):
    message = "This action is restricted to the author only"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsCollab(BasePermission):
    message = "This action is restricted to the collaborators only"

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            project = obj
        elif hasattr(obj, "issue"):
            project = obj.issue.project
        else:
            project = obj.project
        return Contributor.objects.filter(project=project, user=request.user).exists()

    def has_permission(self, request, view):
        project_pk = view.kwargs.get("project_pk")
        if project_pk is None:
            return True
        return Contributor.objects.filter(
            project_id=project_pk, user=request.user
        ).exists()


class IsAuthorOfProject(BasePermission):
    message = "Only the project author can add contributors."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        project_pk = view.kwargs.get("project_pk")
        if project_pk:
            try:
                project = Project.objects.get(pk=project_pk)
            except Project.DoesNotExist:
                return False
            return project.author == request.user
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "issue"):
            return obj.issue.project.author == request.user
        elif hasattr(obj, "project"):
            return obj.project.author == request.user
        elif isinstance(obj, Project):
            return obj.author == request.user
        return False
