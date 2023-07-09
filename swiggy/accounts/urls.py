from django.urls import path
from .views import *

urlpatterns = [
    path('', UserProfile.as_view()),
    path('list', UserList.as_view()),
    path('register', UserCreate.as_view()),
    path('auth', UserLogin.as_view()),
    path('validation', UserValidation.as_view()),
]