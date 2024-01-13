from datetime import timezone

from django.db import models
from user.models import User


# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100)
    fairytale = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.DateTimeField(default=None, null=True)

    def update_date(self):
        self.updated_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'book'

