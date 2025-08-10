"""Serializers de l'App SoftDesk

- Exposent des champs lisibles (ex: author.username) et protègent les champs read-only.
- Appliquent des règles d'intégrité métier côté sérialisation (ex: assignee limité aux contributeurs).
- Fournissent des versions "liste" plus légères pour réduire la charge réseau.
"""
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Project, Issue, Comment
from users.models import User

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors', 'created_time']
        read_only_fields = ['author', 'created_time']

    def create(self, validated_data):
        """Crée un projet et ajoute l'auteur aux contributeurs"""
        contributors = validated_data.pop('contributors', [])
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        project.contributors.set(list(set(contributors + [user])))
        return project

    def update(self, instance, validated_data):
        """Met à jour le projet et garantit que l'auteur reste contributeur, même s'il n'est pas rajouté dans les contributeurs"""
        contributors = validated_data.pop('contributors', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if contributors is not None:
            contributors = list(contributors)
            if instance.author not in contributors:
                contributors.append(instance.author)
            instance.contributors.set(contributors)
        return instance

class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'author']

class IssueSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(), 
        required=False,
        allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author', 'project', 'created_time', 'updated_time']

    def __init__(self, *args, **kwargs):
        """Initialise le queryset de 'assignee' en fonction du projet courant.
        Recherche l'ID du projet dans le contexte (injecté par la vue) ou via
        l'instance (cas PATCH), puis limite 'assignee' aux contributeurs + auteur
        """
        super().__init__(*args, **kwargs)
        project_id = self.context.get('project')
        # Si pas de project_id dans le contexte, on récupère depuis l'instance (cas PATCH)
        if not project_id and self.instance is not None:
            project_id = getattr(self.instance, 'project_id', None)
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
                contributors = list(project.contributors.all())
                if project.author not in contributors:
                    contributors.append(project.author)
                self.fields['assignee'].queryset = User.objects.filter(pk__in=[u.pk for u in contributors])
                self.fields['project'].initial = project_id
            except Project.DoesNotExist:
                self.fields['assignee'].queryset = User.objects.none()
        else:
            self.fields['assignee'].queryset = User.objects.none()

class IssueListSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    assignee = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'status', 'project', 'author', 'assignee']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(read_only=True)
    issue_url = serializers.SerializerMethodField()
    uid = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'issue', 'issue_url', 'uid', 'description']
        read_only_fields = ['author', 'issue', 'created_time', 'updated_time']

    def get_issue_url(self, obj):
        """Retourne l'URL de l'issue liée (absolute si request en contexte)."""
        request = self.context.get('request')
        return reverse('issue-detail', kwargs={'pk': obj.issue_id}, request=request)

    def get_uid(self, obj):
        """Chaîne lisible et unique: "<projet> - <issue> - <id commentaire>"."""
        return f"{obj.issue.project.name} - {obj.issue.title} - {obj.id}"