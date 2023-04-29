import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from books.models import Authors, Books


@pytest.mark.django_db
class TestBookAPI:
    def setup_method(self, method):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.jwt_token = self.get_jwt_token()

    def get_jwt_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        assert response.status_code == 200
        assert 'access' in response.data
        return response.data['access']

    def set_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')

    def test_book_create(self):
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'author': self.user.id,
            'description': 'Test Description',
            'publication_date': '2022-01-01',
        }

        self.set_authorization_header()
        response = self.client.post(url, data)

        assert response.status_code == 201
        assert response.data['title'] == 'Test Book'
        assert Books.objects.count() == 1
        assert Books.objects.filter(author=self.user.id).exists()

    def test_book_list(self):
        url = reverse('book-list')
        self.set_authorization_header()

        response = self.client.get(url)

        assert response.status_code == 200

    def test_book_detail(self):
        author = Authors.objects.create(user=self.user, name='John', surname='Doe', date_of_birth='1990-01-01')
        book = Books.objects.create(title='Test Book', author=author, description='Test Description',
                                    publication_date='2022-01-01')

        self.set_authorization_header()

        url = reverse('book-detail', kwargs={'pk': book.pk})

        response = self.client.get(url)

        assert response.status_code == 200

        book_data = response.data

        assert book_data['title'] == 'Test Book'
        assert book_data['description'] == 'Test Description'
        assert book_data['publication_date'] == '2022-01-01'

        # PUT

        updated_data = {
            'title': 'Updated Book',
            'author': author.id,
            'description': 'Updated Description',
            'publication_date': '2023-01-01',
        }

        response = self.client.put(url, updated_data)

        assert response.status_code == 200

        assert response.data['title'] == 'Updated Book'
        assert response.data['description'] == 'Updated Description'
        assert response.data['publication_date'] == '2023-01-01'

        # DELETE
        response = self.client.delete(url)

        assert response.status_code == 204

        assert not Books.objects.filter(pk=book.pk).exists()
