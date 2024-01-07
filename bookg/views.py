from django.http import HttpResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bookg.serializers import BookSerializer, BookCreateSerializer, UserLoginSerializer, UserSerializer, \
    UserCreateSerializer, UserSignUpSerializer


# Create your views here.

@swagger_auto_schema(method='post', request_body=UserSignUpSerializer)
@api_view(['POST'])
def signup_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': '회원가입 성공!',
        }, status.HTTP_201_CREATED)
    return Response({
        'message': '유효하지 않은 입력값',
        'data': serializer.errors
    }, status.HTTP_400_BAD_REQUEST)

# ligin_user는 어딘가로 렌더링
@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(['POST'])
def login_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': '로그인 성공!',
        }, status.HTTP_201_CREATED)
    return Response({
        'message': '유효하지 않은 입력값',
        'data': serializer.errors
    }, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=BookCreateSerializer)
@api_view(['POST'])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'BookCreateMode',
            'data': serializer.data
        }, status.HTTP_201_CREATED)
    return Response({
        'message': '유효하지 않은 입력값',
        'data': serializer.errors
    }, status.HTTP_400_BAD_REQUEST)



