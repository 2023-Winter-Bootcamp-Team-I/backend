from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from page.models import Page
from book.models import Book
from book.serializers import BookSerializer, BookCreateSerializer, ContentSerializer, ContentChoiceSerializer, \
    TitleCreateSerializer, UserBookListSerializer, UserBookSerializer, DeleteBookSerializer


# 동화책 초기 정보 불러오기
class BaseBook(APIView):
    @swagger_auto_schema(request_body=BookSerializer,
                         responses={201: BookCreateSerializer})
    def post(self, request):
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
        user_id = request.query_params.get('user_id')
        if user_id is not None:
            books = Book.objects.filter(user_id=user_id)
            response_serializer = UserBookListSerializer(books, many=True)
            return Response({
                'result': response_serializer.data
            }, status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class ChoiceContent(APIView):
    @swagger_auto_schema(request_body=ContentSerializer,
                         responses={200: ContentChoiceSerializer})
    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            book_instance = serializer.save()
            response_serializer = ContentChoiceSerializer(book_instance)
            return Response({
                'message': '글 선택 완료',
                'result': response_serializer.data
            }, status.HTTP_200_OK)
        return Response({
            'message': '뭔가 문제 있음',
            'result': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)


# 책 제목을 생성
class TitleCreateTitle(APIView):
    @swagger_auto_schema(request_body=TitleCreateSerializer,
                         responses={200: TitleCreateSerializer})
    def put(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        serializer = TitleCreateSerializer(book, data=request.data)

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


'''
# 동화책 글+그림 정보 불러오는거 만들다 만거어어엉
class CallTextImage(APIView):
    @swagger_auto_schema(request_body=CallTextImageSerializer,
                         responses={200:CallTextImageSerializer})
    def get(self, request, pk, *args, **kwargs):
'''


# 동화책 삭제
class DeleteBookView(APIView):
    @swagger_auto_schema(request_body=DeleteBookSerializer,
                         responses={200: DeleteBookSerializer})
    def delete(self, request, book_id, *args, **kwargs):
        # 동화책 있니 없니
        book_instance = get_object_or_404(Book, pk=book_id)

        book_instance.delete()

        return Response({
            "message": "삭제 완료"
        }, status=status.HTTP_200_OK)


'''
class DeleteBookView(APIView):
    @swagger_auto_schema(request_body=DeleteBookSerializer,
                         responses={200: DeleteBookSerializer})
    def delete(self, request, pk, *args, **kwargs):
        # 동화책 있니 없니
        book_instance = Book.objects.get(id=pk)
        if book_instance == 'POST':
            book_instance.delete()
        return Response({
            "message": "삭제 완료"
        }, status=status.HTTP_200_OK)
'''
'''
class DeleteBookView(APIView):
    @swagger_auto_schema(request_body=DeleteBookSerializer, responses={200: DeleteBookSerializer})
    def delete(self, request, book_id, *args, **kwargs):
        # 동화책 존재 여부 확인
        book_instance = get_object_or_404(Book, pk=book_id)

        # 동화책 및 연결된 페이지 삭제 처리
        book_instance.is_deleted = True
        book_instance.save()

        # 연결된 페이지 삭제 처리
        pages_to_delete = Page.objects.filter(book_id=book_id, is_deleted=False)
        for page in pages_to_delete:
            page.is_deleted = True
            page.save()

        return Response({
            "message": "삭제 완료"
        }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
