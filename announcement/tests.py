from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from announcement.models import Announcement

User = get_user_model()


class AnnouncementAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', email='testuser', name='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_announcement(self):
        url = reverse('api:announcement-list')
        data = {
            'title': 'Test Announcement',
            'content': 'This is a test announcement.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertEqual(Announcement.objects.first().title,
                         'Test Announcement')

    def test_retrieve_update_destroy_announcement(self):
        announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement.',
            user=self.user
        )
        url = reverse('api:announcement-detail',
                      kwargs={'pk': announcement.pk})

        # Retrieve announcement
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Announcement')

        # Update announcement
        data = {
            'title': 'Updated Announcement',
            'content': 'This is an updated announcement.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Announcement')

        # Delete announcement
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Announcement.objects.count(), 0)

    def test_view_count_announcement(self):
        announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement.',
            user=self.user
        )
        url = reverse('api:view_count',
                      kwargs={'pk': announcement.pk})

        # Get view count
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['view_count'], 0)

    def test_my_announcements(self):
        announcement1 = Announcement.objects.create(
            title='Announcement 1',
            content='This is announcement 1.',
            user=self.user
        )
        announcement2 = Announcement.objects.create(
            title='Announcement 2',
            content='This is announcement 2.',
            user=self.user
        )
        url = reverse('api:my-announcements')

        # Get my announcements
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Announcement 2')
        self.assertEqual(response.data[1]['title'], 'Announcement 1')
