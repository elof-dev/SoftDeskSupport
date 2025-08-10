"""
Paramétrage de l'affichage dans la vue admin
"""
from django.contrib import admin
from .models import Project, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author")


class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "author")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "issue", "author")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)