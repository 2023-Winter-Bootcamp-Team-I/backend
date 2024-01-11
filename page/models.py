from django.db import models

from book.models import Book


# Create your models here.
class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    ko_content = models.TextField(max_length=500)
    en_content = models.TextField(max_length=500)
    image_url = models.ImageField(upload_to="", max_length=500)  # upload_to 처리
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)  # 확인바랍니다
