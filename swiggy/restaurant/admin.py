from django.contrib import admin
from .models import Restaurant, RestaurantCuisines

# Register your models here.
admin.site.register([Restaurant, RestaurantCuisines])
