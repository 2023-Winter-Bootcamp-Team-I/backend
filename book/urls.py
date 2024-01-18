from django.urls import path

from backend.urls import schema_view
from .views import (
    BaseBook, ChoiceContent, BookDetail, EmailBookShare
)

from django.urls import re_path
from .write_page import WritePage

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("books/", BaseBook.as_view()),
    path("books/page/", ChoiceContent.as_view()),
    re_path(r"books/$", WritePage.as_asgi()),
    path('books/<int:pk>', BookDetail.as_view(), name='book-title-create'),
    path('books/share', EmailBookShare.as_view()),
]
