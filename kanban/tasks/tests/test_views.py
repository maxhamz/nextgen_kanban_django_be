from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from tasks.models import Task
from datetime import datetime, timedelta


class TaskListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # create 2 test users
        user1 = User.objects.create(
            username="dummyUser1",
            email="dummy1@mail.com",
            password="dummypassword"
        )

        user2 = User.objects.create(
            username="dummyUser2",
            email="dummy2@mail.com",
            password="dummypassword"
        )

        user1.save()
        user2.save()

        # create 6 tasks, split between 2 users,
        # user 1 will get odd numbered tasks, while user 2 get even-numbered tasks.
        no_tasks = 6

        for i in range(no_tasks):
            Task.objects.create(
                created=datetime.now(),
                due_date=(datetime.now() + timedelta(days=2)),
                title=f'Task {i + 1}',
                details=f'Task {i + 1} Details',
                status=Task.TaskStatus['WIP'],
                owner=user1 if i % 2 == 0 else user2  #pythonsy ternary?
            )
    
    def test_throw_401_if_not_logged_in(self):
        response = self.client.get(reverse('task-list'))
        print("what is response?")
        print(response)
        
