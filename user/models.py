from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError('Users must have an Email Address')
#         if not username:
#             raise ValueError('Users must have a Username')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, username, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             username=username,
#         )
#
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
#
#
# class SoftDeleteModel(models.Model):
#     is_deleted = models.BooleanField(default=False)
#
#     class Meta:
#         abstract = True
#
#     def delete(self):
#         self.is_deleted = True
#         self.save()
#
#     def restore(self):
#         self.is_deleted = False
#         self.save()


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  # 이메일 필드가 따로 있네용?
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Null값 이 가능한데...
    is_deleted = models.BooleanField(default=False)  # Null값 이 가능한데... boolean값? NullBoolean쓰지말라는디 우짜지