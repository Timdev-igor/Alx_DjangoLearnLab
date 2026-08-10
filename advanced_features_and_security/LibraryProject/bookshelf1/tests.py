from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Author, Book, Library, Librarian, BookSelection, Post

User = get_user_model()


# ---------------------------------------------------------------------------
# MODEL TESTS
# ---------------------------------------------------------------------------

class CustomUserModelTest(TestCase):
    def test_create_user_defaults_to_member_role(self):
        user = User.objects.create_user(
            username='alice', email='alice@example.com', password='pass1234'
        )
        self.assertEqual(user.role, User.MEMBER)
        self.assertTrue(user.check_password('pass1234'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='bob', email=None, password='pass1234')

    def test_create_superuser_sets_flags(self):
        admin = User.objects.create_superuser(
            username='root', email='root@example.com', password='pass1234'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_rejects_is_staff_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='root2', email='root2@example.com',
                password='pass1234', is_staff=False
            )

    def test_str_returns_username(self):
        user = User.objects.create_user(username='carol', email='carol@example.com', password='x')
        self.assertEqual(str(user), 'carol')


class AuthorBookLibraryModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='George Orwell')
        self.book = Book.objects.create(
            title='1984', author=self.author, publication_year=1949
        )
        self.library = Library.objects.create(name='Central Library')
        self.library.books.add(self.book)

    def test_author_str(self):
        self.assertEqual(str(self.author), 'George Orwell')

    def test_book_str_and_relation(self):
        self.assertEqual(str(self.book), '1984')
        self.assertEqual(self.book.author, self.author)
        self.assertIn(self.book, self.author.books.all())

    def test_book_default_publication_year(self):
        book = Book.objects.create(title='Untitled', author=self.author)
        self.assertEqual(book.publication_year, 2023)

    def test_library_str_and_m2m(self):
        self.assertEqual(str(self.library), 'Central Library')
        self.assertIn(self.book, self.library.books.all())

    def test_book_permissions_registered(self):
        perms = [codename for codename, _ in Book._meta.permissions]
        self.assertIn('can_add_book', perms)
        self.assertIn('can_change_book', perms)
        self.assertIn('can_delete_book', perms)


class LibrarianModelTest(TestCase):
    def test_librarian_str_and_relations(self):
        user = User.objects.create_user(
            username='libuser', email='lib@example.com', password='x', role=User.LIBRARIAN
        )
        library = Library.objects.create(name='West Branch')
        librarian = Librarian.objects.create(user=user, library=library)

        self.assertEqual(str(librarian), 'libuser')
        self.assertEqual(librarian.library, library)
        self.assertIn(librarian, library.librarians.all())

    def test_librarian_one_to_one_enforced(self):
        user = User.objects.create_user(username='dup', email='dup@example.com', password='x')
        library = Library.objects.create(name='Branch A')
        Librarian.objects.create(user=user, library=library)

        with self.assertRaises(Exception):
            Librarian.objects.create(user=user, library=library)


class BookSelectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reader', email='r@example.com', password='x')
        self.author = Author.objects.create(name='Author X')
        self.book = Book.objects.create(title='Book X', author=self.author)

    def test_str(self):
        selection = BookSelection.objects.create(user=self.user, book=self.book)
        self.assertEqual(str(selection), 'reader selected Book X')

    def test_unique_together_enforced(self):
        BookSelection.objects.create(user=self.user, book=self.book)
        with self.assertRaises(Exception):
            BookSelection.objects.create(user=self.user, book=self.book)


class PostModelTest(TestCase):
    def test_post_permissions_registered(self):
        perms = [codename for codename, _ in Post._meta.permissions]
        self.assertIn('can_view', perms)
        self.assertIn('can_create', perms)
        self.assertIn('can_edit', perms)
        self.assertIn('can_delete', perms)


# ---------------------------------------------------------------------------
# VIEW TESTS
# ---------------------------------------------------------------------------

class RoleBasedViewAccessTest(TestCase):
    """Confirms user_passes_test role checks actually gate access."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin1', email='a@example.com', password='pass1234', role=User.ADMIN
        )
        self.librarian = User.objects.create_user(
            username='lib1', email='l@example.com', password='pass1234', role=User.LIBRARIAN
        )
        self.member = User.objects.create_user(
            username='mem1', email='m@example.com', password='pass1234', role=User.MEMBER
        )

    def test_anonymous_user_redirected_from_book_list(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_authenticated_user_can_view_book_list(self):
        self.client.login(username='mem1', password='pass1234')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['can_manage'])

    def test_librarian_can_manage_books_flag(self):
        self.client.login(username='lib1', password='pass1234')
        response = self.client.get(reverse('book_list'))
        self.assertTrue(response.context['can_manage'])

    def test_member_cannot_access_add_book(self):
        self.client.login(username='mem1', password='pass1234')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 302)  # redirected, not authorized

    def test_admin_can_access_add_book(self):
        self.client.login(username='admin1', password='pass1234')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_access_user_list(self):
        self.client.login(username='lib1', password='pass1234')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin1', password='pass1234')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)


class BookCRUDViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin2', email='a2@example.com', password='pass1234', role=User.ADMIN
        )
        self.client.login(username='admin2', password='pass1234')
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Original Title', author=self.author, publication_year=2000
        )

    def test_add_book_creates_record(self):
        response = self.client.post(reverse('add_book'), {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2020,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_edit_book_updates_record(self):
        response = self.client.post(reverse('edit_book', args=[self.book.id]), {
            'title': 'Updated Title',
            'author': self.author.id,
            'publication_year': 2001,
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_delete_book_removes_record(self):
        response = self.client.post(reverse('delete_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_get_shows_confirmation(self):
        response = self.client.get(reverse('delete_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())  # not deleted yet


class SearchBooksViewTest(TestCase):
    def setUp(self):
        author = Author.objects.create(name='Jane Austen')
        Book.objects.create(title='Pride and Prejudice', author=author)
        Book.objects.create(title='Emma', author=author)

    def test_search_filters_by_title(self):
        response = self.client.get(reverse('search_books'), {'q': 'Pride'})
        self.assertEqual(response.status_code, 200)
        titles = [b.title for b in response.context['books']]
        self.assertIn('Pride and Prejudice', titles)
        self.assertNotIn('Emma', titles)

    def test_search_without_query_returns_all(self):
        response = self.client.get(reverse('search_books'))
        self.assertEqual(len(response.context['books']), 2)


class RegistrationViewTest(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'role': 'Member',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.role, 'Member')
        # After successful registration the user should be logged in
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_invalid_data_shows_form_again(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'bad-email',
            'password1': 'x',
            'password2': 'y',
            'role': 'Member',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='bad-email').exists())


class BookSelectionViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='selector', email='s@example.com', password='pass1234'
        )
        self.client.login(username='selector', password='pass1234')
        author = Author.objects.create(name='Author Y')
        self.book = Book.objects.create(title='Selectable Book', author=author)

    def test_select_book_creates_selection(self):
        response = self.client.get(reverse('select_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            BookSelection.objects.filter(user=self.user, book=self.book).exists()
        )

    def test_select_book_twice_does_not_duplicate(self):
        self.client.get(reverse('select_book', args=[self.book.id]))
        self.client.get(reverse('select_book', args=[self.book.id]))
        self.assertEqual(
            BookSelection.objects.filter(user=self.user, book=self.book).count(), 1
        )

    def test_my_selections_lists_only_own_selections(self):
        other_user = User.objects.create_user(
            username='other', email='o@example.com', password='pass1234'
        )
        BookSelection.objects.create(user=other_user, book=self.book)
        self.client.get(reverse('select_book', args=[self.book.id]))

        response = self.client.get(reverse('my_selections'))
        selections = response.context['selections']
        self.assertEqual(selections.count(), 1)
        self.assertEqual(selections.first().user, self.user)


class LibraryViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin3', email='a3@example.com', password='pass1234', role=User.ADMIN
        )
        self.member = User.objects.create_user(
            username='mem3', email='m3@example.com', password='pass1234', role=User.MEMBER
        )
        author = Author.objects.create(name='Author Z')
        self.book = Book.objects.create(title='Library Book', author=author)

    def test_member_cannot_add_library(self):
        self.client.login(username='mem3', password='pass1234')
        response = self.client.get(reverse('add_library'))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_add_library(self):
        self.client.login(username='admin3', password='pass1234')
        response = self.client.post(reverse('add_library'), {
            'name': 'New Library',
            'books': [self.book.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Library.objects.filter(name='New Library').exists())

    def test_library_list_can_manage_flag_admin_only(self):
        Library.objects.create(name='Existing Library')

        self.client.login(username='mem3', password='pass1234')
        response = self.client.get(reverse('library_list'))
        self.assertFalse(response.context['can_manage'])

        self.client.login(username='admin3', password='pass1234')
        response = self.client.get(reverse('library_list'))
        self.assertTrue(response.context['can_manage'])