
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from project.views import ContributorViewSet
from project.views import CommentViewSet
from project.views import IssueViewSet
from project.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contributors', ContributorViewSet) 
router.register(r'comments', CommentViewSet) 
router.register(r'issues', IssueViewSet) 
router.register(r'projects', ProjectViewSet) 

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_pair'),
]
