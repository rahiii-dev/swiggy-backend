from django.db import models
from accounts.models import CustomUser
import restaurant.constants as rest_cosntnts

# Create your models here.
class Restaurant(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurant', null=True)
    name = models.CharField('Name', max_length=250)
    address = models.CharField('Address', max_length=250)
    specials = models.TextField('Restaurant Sepecials', null=True)
    rating = models.DecimalField('Rating', max_digits=2, decimal_places=1, default=0.0)
    slug = models.SlugField('Slug',unique=True, max_length=255, null=True)
    image = models.ImageField('Image', upload_to='restaurant_images/')
    latitude = models.DecimalField('Latitude', max_digits=13, decimal_places=10)
    longitude = models.DecimalField('Longitude', max_digits=13, decimal_places=10)
    opens_at = models.TimeField('Opens At')
    closes_at = models.TimeField('Closes At')
    opened = models.BooleanField('Opened', default=False)
    geofence_id = models.CharField('Geofence', max_length=300)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return f'{self.name} ({self.owner.full_name})'

# Cuisine
class RestaurantCuisines(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='cuisines')
    cuisine = models.CharField('Cuisine', max_length=250, null=True)
    description = models.TextField()
    image = models.ImageField('Image', upload_to='cuisine_images/')
    cuisine_type = models.PositiveSmallIntegerField(choices=rest_cosntnts.CUISINE_TYPE_CHOICES)
    price = models.DecimalField('Price',max_digits=8, decimal_places=2)
    stocks = models.PositiveIntegerField('Stocks', default=0)

    def __str__(self) -> str:
        return f'{self.cuisine} ({self.restaurant.name})'