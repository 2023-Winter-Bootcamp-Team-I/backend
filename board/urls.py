from django.urls import path

from board.views import create_board

urlpatterns = [
    path('',create_board)
]