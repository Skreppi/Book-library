from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from books.models import Authors, Books

from .serializers import BooksSerializers


class BooksViews(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Создать автора или получить существующего автора, связанного с пользователем
        author, created = Authors.objects.get_or_create(user=user, defaults={'name': user.first_name,
                                                                             'surname': user.last_name})

        # Сохранить книгу
        serializer.save(author=author)
