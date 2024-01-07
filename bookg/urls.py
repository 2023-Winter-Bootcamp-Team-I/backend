from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_user),
    path('books/', views.create_book),
    path('signin/', views.login_user)
]