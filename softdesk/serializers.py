from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        Contributor.objects.create(user=user, project=project, role='author', permission='write')
        return project

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role', 'permission']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

    def validate(self, data):
        # Vérifie que l'assignee est bien contributeur du projet
        project = data.get('project') or self.instance.project
        assignee = data.get('assignee')
        if assignee and not Contributor.objects.filter(user=assignee, project=project).exists():
            raise serializers.ValidationError("L'utilisateur assigné doit être contributeur du projet.")
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        # Vérifie que l'auteur est contributeur du projet lié à l'issue
        issue = data.get('issue') or self.instance.issue
        author = data.get('author')
        project = issue.project
        if author and not Contributor.objects.filter(user=author, project=project).exists():
            raise serializers.ValidationError("L'auteur doit être contributeur du projet.")
        return data