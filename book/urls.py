from django.urls import path, include

from .views import (
    BaseBook, ChoiceContent,
)

from django.urls import re_path
from .write_page import WritePage


urlpatterns = [
    path("books/", BaseBook.as_view()),
    path("books/page/", ChoiceContent.as_view()),
    re_path(r"book/$", WritePage.as_asgi()),
]