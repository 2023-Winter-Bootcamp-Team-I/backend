from rest_framework import serializers
from .models import User


# 회원가입
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'password', 'name',]


class UserLoginSerializer(serializers.Serializer):  # 로그인
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
