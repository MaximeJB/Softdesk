from rest_framework import serializers
from accounts.models import CustomUser
from accounts.serializers import UserSerializer
from .models import Comment, Contributor, Issue, Project


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field="username"
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True
    )

    class Meta:
        model = Contributor
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    contributors = ContributorSerializer(
        many=True, read_only=True, source="contributor_set"
    )

    class Meta:
        model = Project
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    attribution = serializers.SlugRelatedField(
        slug_field="username", queryset=CustomUser.objects.all(), required=True
    )
    project = serializers.ReadOnlyField(source="project_id")
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Issue
        fields = "__all__"

    def validate_attribution(self, value):
        view = self.context.get("view")
        project_pk = None
        if view is not None:
            project_pk = view.kwargs.get("project_pk")

        if not project_pk:
            raise serializers.ValidationError("Can't find the project")

        is_contributor = Contributor.objects.filter(
            project_id=project_pk, user=value
        ).exists()
        if not is_contributor:
            raise serializers.ValidationError(
                "User must be contributors of this project"
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    issue = serializers.ReadOnlyField(source="issue.id")

    class Meta:
        model = Comment
        fields = "__all__"
