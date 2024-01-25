from django.core.mail import EmailMessage
from urllib.parse import unquote
from django.http import Http404
from datetime import datetime
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from page.models import Page
from user.models import User
from book.models import Book
from book.serializers import BookSerializer, BookCreateSerializer, PageContentSerializer, PageContentChoiceSerializer, \
    BookTitleCreateSerializer, UserBookListSerializer, DeleteBookSerializer, EmailBookShareSerializer


# 동화책 초기 정보 불러오거나 생성
class BaseBook(APIView):
    @swagger_auto_schema(request_body=BookSerializer,
                         responses={201: BookCreateSerializer})
    def post(self, request):
        # 입력된 동화책 정보를 직렬화하고 저장
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book_instance = serializer.save()
            response_serializer = BookCreateSerializer(book_instance)
            return Response({
                'message': '초기 정보 입력 완료',
                'result': response_serializer.data
            }, status.HTTP_201_CREATED)
        return Response({
            'message': '유효하지 않은 입력값',
            'result': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY, description='사용자 ID', type=openapi.TYPE_INTEGER)
    ], responses={200: UserBookListSerializer})
    def get(self, request):
        # 사용자가 소유한 동화책 리스트를 조회
        user_id = request.query_params.get('user_id')
        if user_id is not None:
            # 사용자 존재 여부 파악
            get_object_or_404(User, pk=user_id)
            books = Book.objects.filter(user_id=user_id, is_deleted=None)
            response_serializer = UserBookListSerializer(books, many=True)
            return Response({
                'result': response_serializer.data
            }, status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


# 동화책 글 선택
class ChoiceContent(APIView):
    @swagger_auto_schema(request_body=PageContentSerializer,
                         responses={200: PageContentChoiceSerializer})
    def post(self, request):
        # 선택된 페이지의 내용을 직렬화하고 저장
        serializer = PageContentSerializer(data=request.data)
        if serializer.is_valid():
            book_instance = serializer.save()
            response_serializer = PageContentChoiceSerializer(book_instance)
            return Response({
                'message': '글 선택 완료',
                'result': response_serializer.data
            }, status.HTTP_200_OK)
        return Response({
            'message': '뭔가 문제 있음',
            'result': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    # 동화책 제목 생성
    @swagger_auto_schema(request_body=BookTitleCreateSerializer,
                         responses={200: BookTitleCreateSerializer})
    def put(self, request, pk, *args, **kwargs):
        # 동화책 제목 생성
        book = get_object_or_404(Book, pk=pk)
        serializer = BookTitleCreateSerializer(book, data=request.data)

        if serializer.is_valid():
            #  serializer.validated_data['user_id'] = request.user.id
            book = serializer.save()
            return Response({
                'message': '책 제목 생성 성공',
                'result': {
                    'book_id': book.book_id,
                    'book_title': serializer.data['title']
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'message': '책 제목 생성 실패',
            'result': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # 동화책 글+그림 불러오기
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description='책 ID', type=openapi.TYPE_INTEGER)
    ], responses={200: PageContentChoiceSerializer})
    def get(self, request, pk, *args, **kwargs):
        # book_id를 기반으로 페이지들을 불러옴
        book = get_object_or_404(Book, pk=pk, is_deleted=None)
        pages = Page.objects.filter(book_id=pk).order_by('page_num')

        # 각 페이지의 내용과 이미지 url을 리스트에 저장
        content_list = []
        for page in pages:
            content_data = {
                'page_num': page.page_num,
                'ko_content': page.ko_content,
                'en_content': page.en_content,
                'ko_tts_url': page.ko_tts_url,
                'en_tts_url': page.en_tts_url,
                # 이미지 선택 안할시 기본 이미지 url 반환
                'image_url': page.image_url if page.image_url else 'https://bookg-s3-bucket.s3.ap-northeast-2.amazonaws.com/UUID.png',
                'created_at': page.created_at,
                'update_at': page.updated_at
            }
            content_list.append(content_data)

        response_data = {
            'book_id': book.book_id,
            'title': book.title,
            'content': content_list
        }

        return Response(response_data, status=status.HTTP_200_OK)

    # 동화책 삭제
    @swagger_auto_schema(responses={200: DeleteBookSerializer})
    def delete(self, request, pk, *args, **kwargs):
        try:
            # 동화책 존재 여부 확인 후 삭제
            book_instance = get_object_or_404(Book, pk=pk)

            # is_deleted 필드를 현재시간으로 설정(소프트딜리트)
            book_instance.is_deleted = datetime.now()
            book_instance.save()

            return Response({
                "message": "삭제 완료"
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "message": "동화책이 존재하지 않습니다."
            }, status=status.HTTP_404_NOT_FOUND)


class EmailBookShare(APIView):
    @swagger_auto_schema(query_serializer=EmailBookShareSerializer)
    def get(self, request):
        # 이메일을 통해 동화책 공유
        serializer = EmailBookShareSerializer(data=request.query_params)
        if serializer.is_valid():
            take = serializer.validated_data['to']           # 받는 사람
            book_id = serializer.validated_data['book_id']

            url = "http://bookg/api/v1/books/"
            url_detail = url + f"{book_id}"
            subject = "소중한 책 선물"                         # 메일 제목
            from_email = "kjy154969@naver.com"               # 보내는 사람
            message = f"{url_detail} 을 통해 공유 된 책을 감상할 수 있어요!"
            EmailMessage(subject=subject, body=message, to=[take], from_email=from_email).send()
            return Response({"message": "이메일 보내기 성공",
                             "result": {
                                 "share_email": f"{url_detail}",
                                 "book_id": book_id
                             }})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
