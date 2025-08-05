from django.db import models
from users.models import User
from django.conf import settings

class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects_contributed')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    STATUS_CHOICES = [
        ('à faire', 'À faire'),
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]
    PRIORITY_CHOICES = [
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('élevée', 'Élevée'),
    ]
    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('tâche', 'Tâche'),
        ('amélioration', 'Amélioration'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField()
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues_created')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issues_assigned')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    custom_id = models.CharField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        if not self.custom_id:
            date_str = self.issue.created_time.strftime('%d%m%Y')
            self.custom_id = f"{self.issue.project.name}_{self.issue.title}_{date_str}".replace(' ', '_')
            super().save(update_fields=['custom_id'])

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.issue.title}"