from django.urls import path, re_path
from book.write_page import WritePage

websocket_urlpatterns = [
    re_path(r"ws/books/$", WritePage.as_asgi()),
]