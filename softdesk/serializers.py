from rest_framework import serializers
from .models import Project, Issue, Comment, User

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors', 'created_time']
        read_only_fields = ['author', 'created_time']

    def create(self, validated_data):
        contributors = validated_data.pop('contributors', [])
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        project.contributors.set(contributors + [user]) 
        return project

class IssueSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.none())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author', 'project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_id = self.context.get('project_id')
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
                self.fields['assignee'].queryset = project.contributors.all()
                self.fields['project'].initial = project_id
                self.fields['project'].read_only = True 
            except Project.DoesNotExist:
                self.fields['assignee'].queryset = User.objects.none()
        else:
            self.fields['assignee'].queryset = User.objects.none()

class CommentSerializer(serializers.ModelSerializer):
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'issue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        issue_id = self.context.get('issue_id')
        if issue_id:
            self.fields['issue'].initial = issue_id
