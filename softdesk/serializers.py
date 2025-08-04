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
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        user = self.context['request'].user
        return Issue.objects.create(author=user, **validated_data)

    def validate(self, data):
        # Vérifie que l'assignee est bien contributeur du projet
        project = data.get('project') or self.instance.project
        assignee = data.get('assignee')
        if assignee and not Contributor.objects.filter(user=assignee, project=project).exists():
            raise serializers.ValidationError("L'utilisateur assigné doit être contributeur du projet.")
        return data

class CommentSerializer(serializers.ModelSerializer):
    issue_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'uuid']

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(author=user, **validated_data)

    def validate(self, data):
        # Vérifie que l'auteur (utilisateur connecté) est contributeur du projet lié à l'issue
        issue = data.get('issue') or self.instance.issue
        author = self.context['request'].user
        project = issue.project
        if not Contributor.objects.filter(user=author, project=project).exists():
            raise serializers.ValidationError("L'auteur doit être contributeur du projet.")
        return data
    
    def get_issue_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/issues/{obj.issue.id}/')
        return f'/api/issues/{obj.issue.id}/'