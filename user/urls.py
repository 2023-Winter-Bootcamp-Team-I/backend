from django.urls import path
from .views import create_user, login_view

urlpatterns = [
    path('users/signup/', create_user, name='signup'),
    path('users/signin/', login_view, name='login'),
]
