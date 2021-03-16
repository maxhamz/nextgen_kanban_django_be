import json
from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase, APIClient  # ,URLPatternsTestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import datetime, timedelta

# client = Client()
NO_TASKS = 6


class TaskListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        # set default user cedentials

        # create 2 test users
        user1 = User.objects.create_user(
            username="dummyUser1",
            email="dummy1@mail.com",
            password="dummypassword"
        )

        user2 = User.objects.create(
            username="dummyUser2",
            email="dummy2@mail.com",
            password="dummypassword"
        )
        user1.is_active = True
        user2.is_active = False

        user1.save()
        user2.save()

        # create 6 tasks, split between 2 users,
        # user 1 will get odd numbered tasks, while user 2 get even-numbered tasks.

        for i in range(NO_TASKS):
            Task.objects.create(
                created=datetime.now(),
                due_date=(datetime.now() + timedelta(days=2)),
                title=f'Task {i + 1}',
                details=f'Task {i + 1} Details',
                status=Task.TaskStatus['WIP'],
                owner=user1 if i % 2 == 0 else user2   # pythonsy ternary?
            )

    def test_throw_401_if_not_logged_in(self):
        response = self.client.get(reverse('task-list'))
        # Check that we got error 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_tasks(self):
        # client = APIClient(enforce_csrf_checks=False)
        url = reverse('token_obtain_pair')
        sampleUser = {
            'username': 'dummyUser1',
            'password': 'dummypassword'
        }

        loginResponse = self.client.post(
            url,
            data=json.dumps(sampleUser),
            content_type='application/json'
        )

        accessToken = loginResponse.data['access']

        self.assertEqual(loginResponse.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + accessToken)

        tasksResponse = self.client.get(reverse('task-list'), format='json')
        # tasksResponseJSON = json.dumps(tasksResponse.data)

        self.assertEqual(tasksResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(len(tasksResponse.data), NO_TASKS)

    def test_post_a_task(self):
        # client = APIClient(enforce_csrf_checks=False)
        url = reverse('token_obtain_pair')
        sampleUser = {
            'username': 'dummyUser1',
            'password': 'dummypassword'
        }

        loginResponse = self.client.post(
            url,
            data=json.dumps(sampleUser),
            content_type='application/json'
        )

        accessToken = loginResponse.data['access']

        self.assertEqual(loginResponse.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + accessToken)

        exampleTaskPost = {
            'title': 'Test Dummy Task 1',
            'details': 'Dummy Task Details Goes Here'
        }

        tasksResponse = self.client.post(
            reverse('task-list'),
            data=json.dumps(exampleTaskPost),
            content_type='application/json'
        )
        # tasksResponseJSON = json.dumps(tasksResponse.data)

        self.assertEqual(tasksResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tasksResponse.data['title'], exampleTaskPost['title'])
        self.assertEqual(
            tasksResponse.data['details'], exampleTaskPost['details'])
