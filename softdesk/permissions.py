"""Permissions personnalisées :

- IsUser: exige un utilisateur authentifié
- IsProjectContributor: accès autorisé si auteur ou contributeur du projet lié
- IsAuthor: modification réservée à l'auteur de l'objet uniqument
"""
from rest_framework import permissions
from .models import Project, Issue, Comment

class IsUser(permissions.BasePermission):
    """Autorise tout utilisateur authentifié."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsProjectContributor(permissions.BasePermission):
    """Autorise l'accès si l'utilisateur est contributeur ou auteur du projet"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, Project):
            return obj.author == user or obj.contributors.filter(pk=user.pk).exists()
        if isinstance(obj, Issue):
            project = obj.project
            return project.author == user or project.contributors.filter(pk=user.pk).exists()
        if isinstance(obj, Comment):
            project = obj.issue.project
            return project.author == user or project.contributors.filter(pk=user.pk).exists()
        return False

    def has_permission(self, request, view):
        """ Pour la création d'issue/comment, vérifie la contribution au projet parent
        via les paramètres ?project= ou ?issue=
        """
        if request.method == "POST":
            project_id = request.query_params.get('project')
            issue_id = request.query_params.get('issue')
            from .models import Project, Issue
            user = request.user
            if project_id:
                try:
                    project = Project.objects.get(pk=project_id)
                except Project.DoesNotExist:
                    return False
                return project.author == user or project.contributors.filter(pk=user.pk).exists()
            if issue_id:
                try:
                    issue = Issue.objects.get(pk=issue_id)
                    project = issue.project
                except Issue.DoesNotExist:
                    return False
                return project.author == user or project.contributors.filter(pk=user.pk).exists()
        return True

class IsAuthor(permissions.BasePermission):
    """Autorise uniquement l'auteur de l'objet"""
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'author') and obj.author == request.user