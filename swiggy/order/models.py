from django.db import models
from accounts.models import CustomUser
from restaurant.models import Restaurant, RestaurantCuisines
import order.constants as ord_const

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ordered_user')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ordered_restaurant')
    order_status = models.PositiveSmallIntegerField(choices=ord_const.ORDER_STATUS, default=ord_const.PENDING)
    latitude = models.DecimalField('Latitude', max_digits=13, decimal_places=10, null=True)
    longitude = models.DecimalField('Longitude', max_digits=13, decimal_places=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.userid}'s order at {self.restaurant.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    cusine = models.ForeignKey(RestaurantCuisines, on_delete=models.CASCADE, related_name='ordered_cusine')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.cusine.cuisine} in {self.order.user.userid}'s order at {self.order.restaurant.name}"
