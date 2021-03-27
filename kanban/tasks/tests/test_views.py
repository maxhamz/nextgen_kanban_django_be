import json
from django.utils import timezone
from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase, APIClient  # ,URLPatternsTestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task, TaskStatus
from datetime import timedelta  # timezone

# client = Client()
NO_TASKS = 6
TEST_USER = {
    'username': 'dummyUser1',
    'password': 'dummypassword'
}
CONTENT_TYPE = 'application/json'
LOGIN_URL = reverse('token_obtain_pair')
ID_TASK_TEST = 6  # for test put & delete


class TaskListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        # set default user credentials

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
                created=timezone.now(),
                due_date=(timezone.now() + timedelta(days=2)),
                title=f'Task {i + 1}',
                details=f'Task {i + 1} Details',
                owner=user1 if i % 2 == 0 else user2   # pythonsy ternary?
            )

    def test_login(self):
        loginResponse = self.client.post(
            LOGIN_URL,
            data=json.dumps(TEST_USER),
            content_type=CONTENT_TYPE
        )

        accessToken = loginResponse.data['access']
        self.assertEqual(loginResponse.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + accessToken)

    def test_throw_401_if_not_logged_in(self):
        response = self.client.get(reverse('task-list'))
        # Check that we got error 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_tasks(self):
        # client = APIClient(enforce_csrf_checks=False)

        self.test_login()

        tasksResponse = self.client.get(reverse('task-list'), format='json')
        # tasksResponseList = list(tasksResponse.data)

        self.assertEqual(tasksResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(len(tasksResponse.data), NO_TASKS)

    def test_post_a_task(self):
        # client = APIClient(enforce_csrf_checks=False)
        self.test_login()

        exampleTaskPost = {
            'title': 'Test Dummy Task 1',
            'details': 'Dummy Task Details Goes Here'
        }

        tasksResponse = self.client.post(
            reverse('task-list'),
            data=json.dumps(exampleTaskPost),
            content_type=CONTENT_TYPE
        )
        # tasksResponseJSON = json.dumps(tasksResponse.data)

        self.assertEqual(tasksResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tasksResponse.data['title'], exampleTaskPost['title'])
        self.assertEqual(
            tasksResponse.data['details'], exampleTaskPost['details'])

    def test_get_a_task(self): 
        self.test_login()

        taskResponse = self.client.get(
            reverse('task-detail', kwargs={'pk': ID_TASK_TEST}),
            format='json'
        )

        self.assertEqual(taskResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(taskResponse.data['id'], ID_TASK_TEST)

    def test_update_a_task(self):
        self.test_login()
        
        # print("\n\n THIS IS THE TASKSTATUS")
        # print(TaskStatus.BACKLOG)

        exampleTaskPut = {
            'title': 'Test Dummy Task 1 UPDATE',
            'details': 'UPDATING Dummy Task Details Goes Here'
        }

        taskResponse = self.client.put(
            reverse('task-detail', kwargs={'pk': ID_TASK_TEST}),
            data=exampleTaskPut,
            format='json'
        )
        print(taskResponse)
        print(taskResponse.data)

        self.assertEqual(taskResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(taskResponse.data['title'], exampleTaskPut['title'])
        self.assertEqual(taskResponse.data['details'], exampleTaskPut['details'])

    def test_delete_a_task(self):
        self.test_login()
        
        # print("\n\n THIS IS THE TASKSTATUS")
        # print(TaskStatus.BACKLOG)

        taskResponse = self.client.delete(
            reverse('task-detail', kwargs={'pk': ID_TASK_TEST}),
            format='json'
        )

        self.assertEqual(taskResponse.status_code, status.HTTP_204_NO_CONTENT)
