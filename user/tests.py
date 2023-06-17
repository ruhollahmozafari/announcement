from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        url = reverse('user:Sign-Up')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'name': 'Test User',
            'password': 'testpassword',
            'mobile': '1234567890'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testuser')

    def test_login_user(self):
        User.objects.create_user(
            username='testuser', email='testuser@example.com', name='testuser', password='testpassword')
        url = reverse('user:Login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_retrieve_update_user_account(self):
        user = User.objects.create_user(
            username='testuser', email='testuser@example.com', name='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        url = reverse('user:get_update_account')
        data = {
            'name': 'Updated User',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated User')

    def test_retrieve_user_account_unauthenticated(self):
        url = reverse('user:get_update_account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
