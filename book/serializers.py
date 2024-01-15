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


# 동화책 전체 리스트 불러오기 api
class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['user_id']


class UserBookListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['book_id', 'title', 'created_at', 'image_url']

    def get_image_url(self, obj):
        # 가장 최근의 페이지를 가져오고, 해당 페이지의 이미지 URL 반환
        page = Page.objects.filter(book_id=obj.book_id).order_by('-created_at').first()
        return page.image_url.url if page else None


class DeleteBookSerializer(serializers.Serializer):
    book_id = serializers

    class Meta:
        model = Book
        fields = ['book_id']


'''
추후에 삭제하겠습니다!
class CallTextImageSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
'''
