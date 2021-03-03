from django.test import TestCase
from tasks.models import Task
from tasks.models.Task import TaskStatus
from datetime import datetime, timedelta

# THIS IS UNIT TEST
# Create your tests here.
class TaskModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Task.objects.create(
            created=datetime.now(),
            title='Test task 1',
            details='Test details goes here',
            status=
        )
        

