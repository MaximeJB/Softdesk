from rest_framework.permissions import BasePermission, SAFE_METHODS
from project.models import Project
from project.models import Contributor


class IsAuthor(BasePermission):
    message = 'This action is restricted to the author only'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
    
class IsCollab(BasePermission):
    message = 'This action is restricted to the collaborators only'
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            project = obj
        else:
            project = obj.project  
        return Contributor.objects.filter(project=project,user=request.user).exists()
    
class IsAuthorOfProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user
        
   