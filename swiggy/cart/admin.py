from django.contrib import admin
from .models import CartItemModel, CartModel

# Register your models here.
admin.site.register([CartItemModel, CartModel])