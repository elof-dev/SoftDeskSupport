from django.contrib import admin
from .models import Project, Issue, Comment


class AutoAuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author') 

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Project, AutoAuthorAdmin)
admin.site.register(Comment, AutoAuthorAdmin)
admin.site.register(Issue, AutoAuthorAdmin)