from rest_framework import serializers

from books.models import Books


class BooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('title', 'description', 'publication_date')
