from rest_framework import serializers

from book.models import Book
from page.models import Page

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['user_id', 'username', 'fairytale', 'gender', 'age']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'username', 'fairytale', 'gender', 'age']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['book_id', 'page_num', 'ko_content', 'en_content']

class ContentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['page_id', 'book_id', 'page_num', 'ko_content', 'en_content']