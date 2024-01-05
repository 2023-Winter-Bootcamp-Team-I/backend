from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  # 이메일 필드가 따로 있네용?
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Null값 이 가능한데...
    is_deleted = models.BooleanField(default=False)  # Null값 이 가능한데... boolean값? NullBoolean쓰지말라는디 우짜지


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)  # Null 값이 가능한데...
    username = models.CharField(max_length=100)
    fairytale = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()  # 비워 놔도 상관 없다
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.DateTimeField(default=None, null=True) # Null값 이 가능한데... boolean값? NullBoolean쓰지말라는디 우짜지


class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_num = models.IntegerField()  # 최대 길이를 6으로 지정하는게 좋을지? 이거 다시 봐주셔야 합니다.
    ko_content = models.TextField(max_length=500)  # 텍스트 필드로 수정 - 수정완료
    en_content = models.TextField(max_length=500)  # 텍스트 필드로 수정 - 수정완료
    image_url = models.ImageField(upload_to="", max_length=500)  # upload_to 처리를 어찌해야될까요...?파일 불러오는 위치를 어디로 해야할지..
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.DateTimeField(default=None, null=True) # Null값 이 가능한데... boolean값? NullBoolean쓰지말라는디 우짜지