import json
from django.utils import timezone
from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase 
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from datetime import timedelta  # timezone

TEST_USER_ZERO = {
    'username': 'dummyUser1',
    'email': 'dummy1@mail.com',
    'password': 'dummypassword'
}
TEST_LOGIN_ZERO = {
    'username': 'dummyUser1',
    'password': 'dummypassword'
}
TEST_USER = {
    'username': 'dummyUser2',
    'password': 'dummypassword',
    'email': 'dummy2@mail.com'
}
TEST_USER1 = {
    'username': 'dummyUser1',
    'password': 'dummypassword',
    'email': 'dummymailcom'
}
CONTENT_TYPE = 'application/json'
REGISTER_URL = reverse('accounts-list')
LOGIN_URL = reverse('token_obtain_pair')
LOGOUT_URL = reverse('accounts-logout')
ID_TASK_TEST = 6  # for test put & delete


class AccountsListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username="dummyUser1",
            email="dummy1@mail.com",
            password="dummypassword"
        )
        user1.is_active = True

        user1.save()

    def test_register_new_user(self):

        new_user_creds = self.client.post(
            REGISTER_URL, 
            data=json.dumps(TEST_USER),
            content_type=CONTENT_TYPE
        )

        self.assertEqual(new_user_creds.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_user_creds.data['username'], TEST_USER['username'])
    
    def test_400_invalid_email_register_new_user(self):
    
        new_user_creds = self.client.post(
            REGISTER_URL, 
            data=json.dumps(TEST_USER1),
            content_type=CONTENT_TYPE
        )
        
        self.assertEqual(new_user_creds.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_all_users(self):
        
        listUsers = self.client.get(REGISTER_URL, format='json')
        
        self.assertEqual(listUsers.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listUsers.data), 1)


class LogoutViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username="dummyUser1",
            email="dummy1@mail.com",
            password="dummypassword"
        )
        user1.is_active = True

        user1.save()

    def test_login(self):
        loginResponse = self.client.post(
            LOGIN_URL,
            data=json.dumps(TEST_LOGIN_ZERO),
            content_type=CONTENT_TYPE
        )

        accessToken = loginResponse.data['access']
        self.assertEqual(loginResponse.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + accessToken)
    
    def test_logout(self):
        
        self.test_login()
        
        logoutResponse = self.client.post(
            LOGOUT_URL,
            data={},
            content_type=CONTENT_TYPE
        )
        
        self.assertEqual(logoutResponse.status_code, status.HTTP_205_RESET_CONTENT)
