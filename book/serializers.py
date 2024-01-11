from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['user_id', 'username', 'fairytale', 'gender', 'age']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'username', 'fairytale', 'gender', 'age']