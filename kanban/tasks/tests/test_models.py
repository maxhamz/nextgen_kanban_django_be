from django.test import TestCase
from tasks.models import Task
from django.db import models
from django.contrib.auth.models import User
# from .models import Task
from datetime import datetime, timedelta

# THIS IS UNIT TEST
# Create your tests here.


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # SINCE THERE IS FOREIGN KEY OF USER, LET'S CREATE USER FIRST
        user = User.objects.create(
            username="dummyUser1",
            email="dummy@mail.com",
            password="dummypassword"
        )

        Task.objects.create(
            created=datetime.now(),
            # due_date=models.DateTimeField(
            #     datetime.now() + timedelta(days=2)
            # ),
            title='Test task 1',
            details='Test details goes here',
            # status='WIP',
            owner=user
        )

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_details_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('details').verbose_name
        self.assertEqual(field_label, 'details')

    def test_owner_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'owner')

    def test_created_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'created')
