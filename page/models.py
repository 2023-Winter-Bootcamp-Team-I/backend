from datetime import timezone

from django.db import models

from book.models import Book


# Create your models here.
class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_num = models.IntegerField()  # 최대 길이를 6으로 지정하는게 좋을지? 이거 다시 봐주셔야 합니다.
    ko_content = models.TextField(max_length=500)  # 텍스트 필드로 수정 - 수정완료
    en_content = models.TextField(max_length=500)  # 텍스트 필드로 수정 - 수정완료
    image_url = models.ImageField(upload_to="", max_length=500)  # upload_to 처리를 어찌해야될까요...?파일 불러오는 위치를 어디로 해야할지..
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.DateTimeField(default=None, null=True)

    def update_date(self):
        self.updated_at = timezone.now()
        self.save()
    class Meta:
        db_table = 'page'