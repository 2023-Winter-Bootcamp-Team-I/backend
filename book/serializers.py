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


class TitleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title']

'''
동화책 글+그림 정보 불러오는거 만들다 만거어어엉
class CallTextImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['book_id']
'''


class DeleteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id']
