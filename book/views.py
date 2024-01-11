from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from book.serializers import BookSerializer, BookCreateSerializer

#동화책 초기 정보 불러오기
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
                'data': response_serializer.data
            }, status.HTTP_201_CREATED)
        return Response({
            'message': '유효하지 않은 입력값',
            'data': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)

