from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a user for authentication
        self.user = User.objects.create_user(username='tim', password='library123')
        self.client = APIClient()

        # Log in the user using Django's login method
        self.client.login(username='tim', password='library123')

        # Create a sample book with real-world examples
        self.book = Book.objects.create(
            title='deathnote',
            author='Kojima',
            publication_year=2020,
            isbn='9780061120084'
        )

    def test_create_book(self):
        """
        Ensure we can create a new book.
        """
        url = reverse('book-list')
        data = {
            'title': 'harrypotter',
            'author': 'George Orwell',
            'publication_year': 2006,
            'isbn': '9780451524935'
        }
        response = self.client.post(url, data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response data
        self.assertEqual(response.data['title'], 'harrypotter')
        self.assertEqual(response.data['author'], 'George Orwell')
        self.assertEqual(response.data['publication_year'], 2006)
        self.assertEqual(response.data['isbn'], '9780451524935')

        # Check if the book was saved in the database
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        """
        Ensure we can retrieve a book.
        """
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(response.data['title'], 'deathnote')
        self.assertEqual(response.data['author'], 'Kojima')
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['isbn'], '9780061120084')

    def test_update_book(self):
        """
        Ensure we can update a book.
        """
        url = reverse('book-detail', args=[self.book.id])
        data = {
            'title': 'deathnote',
            'author': 'Kojima',
            'publication_year': 2020,
            'isbn': '9780061120084',
            'genre': 'sci'  # Adding a new field for demonstration
        }
        response = self.client.put(url, data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(response.data['title'], 'deathnote')
        self.assertEqual(response.data['author'], 'Kojima')
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['isbn'], '9780061120084')
        self.assertEqual(response.data['genre'], 'Classic')  # Verify the new field

        # Check if the book was updated in the database
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.title, 'deathnote')

    def test_delete_book(self):
        """
        Ensure we can delete a book.
        """
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the book was deleted from the database
        self.assertEqual(Book.objects.count(), 0)

    def test_list_books(self):
        """
        Ensure we can list all books.
        """
        url = reverse('book-list')
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(len(response.data), 1)  # Only one book exists
        self.assertEqual(response.data[0]['title'], 'deathnote')
        self.assertEqual(response.data[0]['author'], 'Kojima')
        self.assertEqual(response.data[0]['publication_year'], 2020)
        self.assertEqual(response.data[0]['isbn'], '9780061120084')

    def test_filter_books_by_author(self):
        """
        Ensure we can filter books by author.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'Kojima'})

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(len(response.data), 1)  # Only one book matches the filter
        self.assertEqual(response.data[0]['title'], 'deathnote')

    def test_unauthenticated_access(self):
        """
        Ensure unauthenticated users cannot access protected endpoints.
        """
        # Log out the authenticated user
        self.client.logout()

        # Make a request to a protected endpoint
        url = reverse('book-list')
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Or 401, depending on your setup