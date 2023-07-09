from django.urls import path
from .views import *

urlpatterns = [
    path("", CartView.as_view()),
    path("cusine/<int:id>", CusineCartDetails.as_view()),
    path("count/", CartItemsCount.as_view()),
    path("change/", ChangeCart.as_view())
]