from rest_framework import serializers
from .models import Contributor
from .models import Comment
from .models import Project
from .models import Issue
from accounts.serializers import UserSerializer
from accounts.models import CustomUser

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(),slug_field='username')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    
    class Meta:
        model = Contributor
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True, source='contributor_set')
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    attribution = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all(), required=True)


    class Meta:
        model = Comment
        fields = '__all__'




