from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Task(models.Model):
    
    # status is enum
    class TaskStatus(models.TextChoices):
        BACKLOG = 'LOG', _('Backlog')
        CREATED = 'CRT', _('Created')
        WIP = 'WIP', _('In Progress')
        DONE = 'DON', _('Done')
    
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False)
    details = models.TextField()
    status = models.CharField(
        max_length=3,
        choices=TaskStatus.choices,
        default=TaskStatus.CREATED
    )
    due_date = models.DateTimeField(
        default=(datetime.now() - timedelta(days=2))
    )
    owner = models.ForeignKey(
        'auth.user',
        related_name='tasks',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created', 'due_date']
