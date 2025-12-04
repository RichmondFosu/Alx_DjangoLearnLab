from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')

        # Create books
        self.book1 = Book.objects.create(title='Book One', publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2021, author=self.author2)

        # API client
        self.client = APIClient()

    # -------------------- LIST BOOKS --------------------
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -------------------- RETRIEVE BOOK --------------------
    def test_retrieve_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.author1.id)

    # -------------------- CREATE BOOK --------------------
    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {'title': 'Book Three', 'publication_year': 2022, 'author': self.author1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='Book Three').author, self.author1)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {'title': 'Book Four', 'publication_year': 2022, 'author': self.author2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_duplicate_title(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {'title': self.book1.title, 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------- UPDATE BOOK --------------------
    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Book One'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    def test_update_book_unauthenticated(self):
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Fail Update'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------- DELETE BOOK --------------------
    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': self.book2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_delete_book_unauthenticated(self):
        url = reverse('book-delete', kwargs={'pk': self.book2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------- FILTERING / SEARCH / ORDERING --------------------
    def test_filter_books_by_author(self):
        url = reverse('book-list') + f'?author={self.author1.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)

    def test_filter_books_by_author_and_year(self):
        url = reverse('book-list') + f'?author={self.author1.id}&publication_year=2020'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_search_books_partial(self):
        url = reverse('book-list') + '?search=Book'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)  # Both Book One and Book Two

    def test_search_books_exact(self):
        url = reverse('book-list') + '?search=Book Two'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_order_books_by_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    def test_order_books_by_title_asc(self):
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.data[0]['title'], 'Book One')
