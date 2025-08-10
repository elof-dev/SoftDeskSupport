"""ViewSets de l'API SoftDesk.

- Sécurité: permissions par action (CRUD)
- select_related/prefetch_related pour éviter le N+1.
- Pagination: ordre de tri (-created_time, id)
- Hiérarchie: ParentLookupMixin lie les ressources enfants au parent via un query param (?project= / ?issue=)
"""
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
    """
    - Liste restreinte aux contributeurs/auteur
    - Suppression logique (soft-delete)
    """
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        """Retourne un serializer minimal pour la liste, et complet autrement."""
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        """Queryset des projets visibles par l'utilisateur courant.

        - Filtre: auteur OU contributeur; exclut les projets soft-deletés.
        - Optimisations aller-retour BDD: select_related (FK) et prefetch_related (M2M)
        """
        user = self.request.user
        return (
            Project.objects
            .filter(is_deleted=False)
            .filter(Q(author=user) | Q(contributors=user))
            .select_related('author')          
            .prefetch_related('contributors') 
            .order_by('-created_time', 'id') 
            .distinct()
        )

    def get_permissions(self):
        """Permissions par action:
        - create: utilisateur authentifié
        - update/partial_update/destroy: uniquement l'auteur du projet
        - list/retrieve: contributeur ou auteur du projet
        """
        if self.action == 'create':
            return [IsUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        else:  # 'list', 'retrieve'
            return [IsProjectContributor()]

    def perform_destroy(self, instance):
        """Effectue une suppression logique (soft delete)"""
        instance.is_deleted = True
        instance.save()

class IssueViewSet(ParentLookupMixin, viewsets.ModelViewSet):
    """
    Le parent est passé via le paramètre de requête ?project= et injecté par
    ParentLookupMixin lors de la création
    """
    serializer_class = IssueSerializer
    url_param_name = 'project'
    filter_field_name = 'project_id'
    parent_model = Project
    parent_attribute = 'project'

    def get_serializer_class(self):
        """Serializer minimal pour list, complet sinon"""
        if self.action == 'list':
            return IssueListSerializer
        return IssueSerializer

    def get_queryset(self):
        """Issues visibles par l'utilisateur, filtrées par ?project=
        via  auteur/contributeur du projet parent
        """
        user = self.request.user
        project_id = self.request.query_params.get('project')
        queryset = Issue.objects.select_related('project', 'author', 'assignee') 
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        queryset = queryset.filter(
            Q(project__author=user) | Q(project__contributors=user),
            project__is_deleted=False
        ).order_by('-created_time', 'id').distinct()
        return queryset

    def get_permissions(self):
        """Permissions par action:

        - create: contributeur du projet
        - update/partial_update/destroy: uniquement l'auteur de l'issue
        - list/retrieve: contributeur/auteur du projet parent
        """
        if self.action == 'create':
            return [IsProjectContributor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        else:  # 'list', 'retrieve'
            return [IsProjectContributor()]

class CommentViewSet(ParentLookupMixin, viewsets.ModelViewSet):
    """Gestion des commentaires rattachés à une issue:

    Le parent est passé via le paramètre de requête ?issue= et injecté par
    ParentLookupMixin lors de la création
    """
    serializer_class = CommentSerializer
    url_param_name = 'issue'
    filter_field_name = 'issue_id'
    parent_model = Issue
    parent_attribute = 'issue'

    def get_serializer_class(self):
        """Actuellement même serializer pour list et détail"""
        if self.action == 'list':
            return CommentSerializer
        return CommentSerializer

    def get_queryset(self):
        """Commentaires visibles par l'utilisateur, filtrés par ?issue=
        - Optimisations: select_related sur 'issue', 'author' et 'issue__project'
        - Filtre d'accès: contributeur/auteur du projet parent
        """
        user = self.request.user
        issue_id = self.request.query_params.get('issue')
        queryset = Comment.objects.select_related('issue', 'author', 'issue__project') 
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        queryset = queryset.filter(
            Q(issue__project__author=user) | Q(issue__project__contributors=user),
            issue__project__is_deleted=False
        ).order_by('-created_time', 'id').distinct()
        return queryset

    def get_permissions(self):
        """Permissions par action:
        - create: contributeur du projet de l'issue (via ?issue=)
        - update/partial_update/destroy: uniquement l'auteur du commentaire
        - list/retrieve: contributeur/auteur du projet parent
        """
        if self.action == 'create':
            return [IsProjectContributor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        else:  # 'list', 'retrieve'
            return [IsProjectContributor()]