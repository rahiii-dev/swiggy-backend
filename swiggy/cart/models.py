from django.db import models
from restaurant.models import RestaurantCuisines, Restaurant

# Create your models here.    
class CartModel(models.Model):
    userid = models.CharField(verbose_name='Userid',null=True, max_length=300, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if(self.restaurant):
            return f"{self.userid}'s cart at {self.restaurant.name}"
        
        return f"{self.userid}'s cart"

    def item_total(self):
        return sum(cart_item.total_price() for cart_item in self.cartItems.all())

class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='cart_items')
    cuisine = models.ForeignKey(RestaurantCuisines, on_delete=models.CASCADE, related_name='cuisin')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.cuisine.cuisine} in {self.cart.userid}'s"
    
    def total_price(self):
        return self.quantity * float(self.cuisineId.price)
