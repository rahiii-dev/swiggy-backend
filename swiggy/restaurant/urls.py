from django.urls import path
from .views import *

urlpatterns = [
    path('', UserRestaurantView.as_view()),
    path('user/cuisine/<slug:slug>', UserCusinetView.as_view()),

    path('<slug:slug>', UserRestaurantView.as_view()),
    path('register/', RestaurantRegisterView.as_view()),

    path('cuisine/', CuisineView.as_view()),
    path('cuisine/<int:id>', CuisineView.as_view()),

    path('profile/', RestaurantProfileView.as_view()),
    path('zones/', ALLRestaurantZones.as_view()),
    path('validation/', RestaurantValidator.as_view())
]