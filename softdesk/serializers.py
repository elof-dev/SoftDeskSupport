from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment, User

class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time', 'contributors']
        read_only_fields = ['author', 'created_time', 'contributors']

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        Contributor.objects.create(user=user, project=project, role='author', permission='write')
        return project
    
    def get_contributors(self, obj):
        contributors = Contributor.objects.filter(project=obj)
        # On retourne une liste d'utilisateurs (ou d'IDs, ou de usernames selon le besoin)
        return [
            {
                "id": c.user.id,
                "username": c.user.username,
                "role": c.role,
                "permission": c.permission
            }
            for c in contributors
        ]

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=False, is_superuser=False),
    )

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']  # On n'expose plus role ni permission

    def create(self, validated_data):
        # On fixe automatiquement le rôle et la permission
        return Contributor.objects.create(
            **validated_data,
            role='contributor',
            permission='write'
        )

    def validate(self, data):
        project = data.get('project') or self.instance.project
        user = data.get('user') or self.instance.user
        if user == project.author:
            raise serializers.ValidationError("L'auteur du projet est déjà contributeur et ne peut pas être ajouté à nouveau.")
        return data

class IssueSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.none())

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        project_ids = Contributor.objects.filter(user=user).values_list('project_id', flat=True)
        self.fields['project'].queryset = Project.objects.filter(id__in=project_ids)

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
        project_ids = Contributor.objects.filter(user=user).values_list('project_id', flat=True)
        issue_ids = Issue.objects.filter(project_id__in=project_ids).values_list('id', flat=True)
        self.fields['issue'].queryset = Issue.objects.filter(id__in=issue_ids)

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(author=user, **validated_data)