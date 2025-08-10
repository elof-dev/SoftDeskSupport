from rest_framework import viewsets
from .models import Project, Issue, Comment
from .serializers import (
    ProjectSerializer, IssueSerializer, CommentSerializer,
    ProjectListSerializer, IssueListSerializer, CommentSerializer
)
from .permissions import IsUser, IsProjectContributor, IsAuthor
from .mixins import ParentLookupMixin
from django.db.models import Q

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        # retrieve/create/update/destroy -> serializer complet
        return ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects
            .filter(is_deleted=False)
            .filter(Q(author=user) | Q(contributors=user))
            .select_related('author')           # FK
            .prefetch_related('contributors')   # M2M
            .order_by('-created_time', 'id')     # ordre stable
            .distinct()
        )

    def get_permissions(self):
        if self.action == 'create':
            return [IsUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        else:  # 'list', 'retrieve'
            return [IsProjectContributor()]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class IssueViewSet(ParentLookupMixin, viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    url_param_name = 'project'
    filter_field_name = 'project_id'
    parent_model = Project
    parent_attribute = 'project'

    def get_serializer_class(self):
        if self.action == 'list':
            return IssueListSerializer
        return IssueSerializer

    def get_queryset(self):
        user = self.request.user
        project_id = self.request.query_params.get('project')
        queryset = Issue.objects.select_related('project', 'author', 'assignee')  # FK optimisés
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        queryset = queryset.filter(
            Q(project__author=user) | Q(project__contributors=user),
            project__is_deleted=False
        ).order_by('-created_time', 'id').distinct()
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsProjectContributor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        else:  # 'list', 'retrieve'
            return [IsProjectContributor()]

class CommentViewSet(ParentLookupMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    url_param_name = 'issue'
    filter_field_name = 'issue_id'
    parent_model = Issue
    parent_attribute = 'issue'

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        return CommentSerializer

    def get_queryset(self):
        user = self.request.user
        issue_id = self.request.query_params.get('issue')
        queryset = Comment.objects.select_related('issue', 'author', 'issue__project')  # FK + chainé
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        queryset = queryset.filter(
            Q(issue__project__author=user) | Q(issue__project__contributors=user),
            issue__project__is_deleted=False
        ).order_by('-created_time', 'id').distinct()
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsProjectContributor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        else:  # 'list', 'retrieve'
            return [IsProjectContributor()]