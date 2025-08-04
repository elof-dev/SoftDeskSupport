from rest_framework import serializers
from .models import Project, Issue, Comment, User

class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(is_staff=False, is_superuser=False)
    )
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors', 'created_time']
        read_only_fields = ['author', 'created_time']

    def create(self, validated_data):
        contributors = validated_data.pop('contributors', [])
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        project.contributors.set(contributors + [user])  # L'auteur est aussi contributeur
        return project


class IssueSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.none())

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['project'].queryset = Project.objects.filter(contributors=user)

    def create(self, validated_data):
        user = self.context['request'].user
        return Issue.objects.create(author=user, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.none())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'uuid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        issue_ids = Issue.objects.filter(project__contributors=user).values_list('id', flat=True)
        self.fields['issue'].queryset = Issue.objects.filter(id__in=issue_ids)

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(author=user, **validated_data)