from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import user


# Create your views here.

#동화책 초기 정보 불러오기
class BaseBook(APIView):
    # @swagger_auto_schema(
    #     operation_description="지원 정보와 연결된 질문, 답변, 음성파일 받기",
    #     operation_id="질문, 답변, 음성파일 요청",
    # )
    def post(self,request):
        user_id = request.GET.get("user_id")
        # form Object 얻기
        user_object = user.objects.get(id=user_id)

        return Response({"message":"우엥 채워주세오"},status=status.HTTP_200_OK)
