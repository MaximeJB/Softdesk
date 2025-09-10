from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import UserViewSet
from project.views import (
    CommentViewSet,
    ContributorViewSet,
    IssueViewSet,
    ProjectViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"projects", ProjectViewSet)

projects_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
projects_router.register(r"issues", IssueViewSet, basename="project-issues")
projects_router.register(r"contributors", ContributorViewSet, basename="project-contributors")

issues_router = routers.NestedDefaultRouter(projects_router, r"issues", lookup="issue")
issues_router.register(r"comments", CommentViewSet, basename="issue-comment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh_pair",
    ),
    path(
        "projects/<int:project_id>/issues/",
        IssueViewSet.as_view({"get": "list", "post": "create"}),
        name="list_issues",
    ),
    path(
        "issues/<int:pk>/",
        IssueViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="get_delete_object",
    ),
]
