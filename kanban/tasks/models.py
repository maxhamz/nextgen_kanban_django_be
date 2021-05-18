from django.db import models
from datetime import timedelta
from django.utils import timezone
# from django.contrib.auth import get_user_model
from enumfields import EnumField
from enum import Enum
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


# class TaskStatus(models.TextChoices):
#     BACKLOG = 'LOG', 'Backlog'
#     CREATED = 'CRT', 'Created'
#     WIP = 'WIP', 'In Progress'
#     DONE = 'DON', 'Done'

class TaskStatus(Enum):
    BACKLOG = 'LOG'
    CREATED = 'CRT'
    IN_PROGRESS = 'WIP'
    DONE = 'DON'


class Task(models.Model):
    # status is enum
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False)
    details = models.TextField()
    # status = models.CharField(
    #     max_length=3,
    #     choices=TaskStatus.choices,
    #     default=TaskStatus.CREATED
    # )
    status = EnumField(TaskStatus, max_length=3, default=TaskStatus.CREATED)
    due_date = models.DateTimeField(
        default=(timezone.now() + timedelta(days=2))
    )
    owner = models.ForeignKey(
        'auth.User',
        # settings.AUTH_USER_MODEL,
        related_name='tasks',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created', 'due_date']
