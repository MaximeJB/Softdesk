from rest_framework.permissions import SAFE_METHODS, BasePermission
from project.models import Contributor, Project


class IsAuthor(BasePermission):
    """
    Permission class

    Safe methods are always allowed
    Other methods : are only allowed if the requesting user is the author of the object
    """
    message = "This action is restricted to the author only"
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsCollab(BasePermission):
    """
    Permission class

    - If the object is a Project, checks if the user is a contributor.
    - If the object has 'issue' or 'project' attributes, resolves the project
          and checks contributor status.
    - For general permission (list/create), checks if user is a contributor
          of the project identified by 'project_pk' in the URL.
    """
    message = "This action is restricted to the collaborators only"

    def has_object_permission(self, request, view, obj):
        project = getattr(obj, "project", None)
        if project is None:
            issue = getattr(obj, "issue", None)
            if issue is not None:
                project = getattr(issue, "project", None)

        if project is None:
            return False
        return Contributor.objects.filter(project=project, user=request.user).exists()

    def has_permission(self, request, view):
        project_pk = view.kwargs.get("project_pk")
        if project_pk is None:
            return True
        return Contributor.objects.filter(
            project_id=project_pk, user=request.user
        ).exists()


class IsAuthorOfProject(BasePermission):
    """
    Permission class only the project author can manage contributors

    safe methods are always allowed
    unsafe methods, only the author can add or remove contributors
    """
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
        project = getattr(obj, "project", None)

        if project is None:
            issue = getattr(obj, "issue", None)
            if issue is not None:
                project = getattr(issue, "project", None)

        if project is None:
            return False

        return project.author == request.user
