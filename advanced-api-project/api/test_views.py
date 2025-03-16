from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a sample book
        self.book = Book.objects.create(
            title='Sample Book',
            author='Sample Author',
            publication_year=2021,
            isbn='1234567890123'
        )

    def test_create_book(self):
        """
        Ensure we can create a new book.
        """
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023,
            'isbn': '9876543210123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Check if the book was added

    def test_retrieve_book(self):
        """
        Ensure we can retrieve a book.
        """
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Book')

    def test_update_book(self):
        """
        Ensure we can update a book.
        """
        url = reverse('book-detail', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2022,
            'isbn': '1234567890123'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')

    def test_delete_book(self):
        """
        Ensure we can delete a book.
        """
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Check if the book was deleted

    def test_filter_books(self):
        """
        Ensure we can filter books by publication year.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2021})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book matches the filter

    def test_unauthenticated_access(self):
        """
        Ensure unauthenticated users cannot access protected endpoints.
        """
        self.client.logout()  # Log out the authenticated user
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)