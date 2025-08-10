from rest_framework import serializers
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
        contributors = validated_data.pop('contributors', [])
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        project.contributors.set(list(set(contributors + [user])))
        return project

    def update(self, instance, validated_data):
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

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'issue', 'created_time', 'updated_time']