from rest_framework import viewsets
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_id'] = self.request.query_params.get('project')
        return context

    def perform_create(self, serializer):
        project_id = self.request.query_params.get('project')
        project = Project.objects.get(pk=project_id) if project_id else None
        serializer.save(author=self.request.user, project=project)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.request.query_params.get('issue')
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['issue_id'] = self.request.query_params.get('issue')
        return context

    def perform_create(self, serializer):
        issue_id = self.request.query_params.get('issue')
        issue = Issue.objects.get(pk=issue_id) if issue_id else None
        serializer.save(author=self.request.user, issue=issue)