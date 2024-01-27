from rest_framework import serializers
from book.models import Book
from page.models import Page


# 동화책 정보 직렬화
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['user_id', 'username', 'fairytale', 'gender', 'age']


# 동화책 정보 직렬화
class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'username', 'fairytale', 'gender', 'age']


# 페이지 내용을 직렬화
class PageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['book_id', 'page_num', 'ko_content', 'en_content']


# 페이지 내용을 선택할 때 직렬화
class PageContentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['page_id', 'book_id', 'page_num', 'ko_content', 'en_content', 'ko_tts_url', 'en_tts_url', 'created_at', 'updated_at']


class BookTitleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title']


# 동화책 전체 리스트 불러오기
class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['user_id']


# 사용자의 동화책 리스트를 가져오기
class UserBookListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['book_id', 'title', 'created_at', 'image_url']

    def get_image_url(self, obj):
        # 가장 최근의 페이지를 가져오고, 해당 페이지의 이미지 URL 반환
        page = Page.objects.filter(book_id=obj.book_id).order_by('-created_at').first()
        return page.image_url if page and page.image_url else 'https://bookg-s3-bucket.s3.ap-northeast-2.amazonaws.com/UUID.png'


class DeleteBookSerializer(serializers.Serializer):
    book_id = serializers

    class Meta:
        model = Book
        fields = ['book_id']


# 이메일로 동화책 공유
class EmailBookShareSerializer(serializers.Serializer):
    to = serializers.EmailField()
    book_id = serializers.IntegerField()
