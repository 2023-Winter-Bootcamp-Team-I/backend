from rest_framework import serializers

from bookg.models import User, Book


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'password', 'email', 'name', 'created_at', 'updated_at', 'is_deleted']

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'password', 'email', 'name', 'created_at', 'updated_at', 'is_deleted']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'user_id', 'title', 'username', 'fairytale', 'gender', 'age', 'created_at', 'updated_at', 'is_deleted']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id','user_id', 'username', 'fairytale', 'gender', 'age']