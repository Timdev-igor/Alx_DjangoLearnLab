from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create  book
        self.book = Book.objects.create(
            title='Sample Book',
            author='Sample Author',
            publication_year=2021,
            isbn='1234567890123'
        )

    def test_authenticated_access(self):
        """
        Ensure an authenticated user can access protected endpoints.
        """
        # Log in  user
        self.client.login(username='testuser', password='testpass123')

        # Make a request to an endpoint
        url = reverse('book-list')  # Replace with your actual URL name
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        """
        Ensure an unauthenticated user cannot access protected endpoints.
        """
        # Log out the user (if logged in)
        self.client.logout()

        # Make a request to a protected endpoint
        url = reverse('book-list')  # Replace with your actual URL name
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Or 401, depending on your setup