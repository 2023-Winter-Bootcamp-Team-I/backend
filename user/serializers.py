from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):  # 회원가입
    class Meta:
        model = User
        fields = ['user_id', 'password', 'email', 'name',]


class UserLoginSerializer(serializers.Serializer):  # 로그인
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
