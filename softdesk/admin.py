from django.contrib import admin
from .models import Project, Issue, Comment
from users.models import User

admin.site.register(User)

class AutoAuthorAdmin(admin.ModelAdmin):
    exclude = ['author']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Project, AutoAuthorAdmin)
admin.site.register(Comment, AutoAuthorAdmin)
admin.site.register(Issue, AutoAuthorAdmin)