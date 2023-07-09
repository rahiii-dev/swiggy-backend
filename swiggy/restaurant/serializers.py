from rest_framework import serializers
from .models import Restaurant, RestaurantCuisines
import restaurant.constants as rest_const
from .functions import convert_to_12hr
from django.conf import settings

# Register
class RestaurantsRegisterSerializer(serializers.ModelSerializer):
    required_field_validation = ['name', 'address', 'slug', 'image', 'latitude', 'longitude', 'geofence_id', 'specials']

    class Meta:
        model = Restaurant
        fields = '__all__'
    
    def validate(self, data):
        for field in self.required_field_validation:
            if field not in data:
                raise serializers.ValidationError({'message': f"{field} is required"})
        
        return data

class CusineAddSerializer(serializers.ModelSerializer):
    required_field_validation = ['restaurant', 'cuisine', 'image', 'cuisine_type', 'price']
    class Meta:
        model = RestaurantCuisines
        fields = '__all__'
    
    def validate(self, data):
        for field in self.required_field_validation:
            if field not in data:
                raise serializers.ValidationError({'message': f"{field} is required"})
        
        return data

# View    
class RestaurantCuisineSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantCuisines
        exclude = ['restaurant']

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        imageValue = rep.get('image')
        rep['image'] = f'{settings.DOMAIN_NAME}{imageValue}'

        CsnTypeValue = rep.get('cuisine_type')
        for cuisine in rest_const.CUISINE_TYPE_CHOICES:
            if CsnTypeValue == cuisine[0]:
                rep['cuisine_type'] = cuisine[1]

        return rep            

class RestaurantProfileSerializer(serializers.ModelSerializer):
    cuisines = RestaurantCuisineSerializer(many=True, read_only=True) 
    image = serializers.SerializerMethodField('get_image_url')
    location = serializers.SerializerMethodField('get_location')

    class Meta:
        model = Restaurant
        exclude = ['id', 'latitude', 'longitude']
    
    def get_image_url(self, obj):
        return f'{settings.DOMAIN_NAME}{obj.image.url}'

    def get_location(self, obj):
        latitude = obj.latitude
        longitude = obj.longitude
        location = {
            "latitude": latitude,
            "longitude": longitude,
        }
        return location
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        for field in ['opens_at', 'closes_at']:
            try:
                value = rep.get(field)
                rep[field] = convert_to_12hr(value)
            except Exception:
                pass
        
        try:
            value = rep.get('rating')
            rep['rating'] = float(value)
        except Exception:
                pass        

        return rep


# UserArea
from .functions import getETA
from cart.models import CartItemModel, CartModel
from cart.serializers import CartItemSerializer

class UserCuisineSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url', read_only=True)
    cart_details = serializers.JSONField(default=None)

    class Meta:
        model = RestaurantCuisines
        exclude = ['restaurant']
    
    def get_image_url(self, obj):
        return f'{settings.DOMAIN_NAME}{obj.image.url}'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        CsnTypeValue = rep.get('cuisine_type')
        for cuisine in rest_const.CUISINE_TYPE_CHOICES:
            if CsnTypeValue == cuisine[0]:
                rep['cuisine_type'] = cuisine[1]


        return rep

    
class UserRestaurantViewSerializer(RestaurantProfileSerializer):
    cuisines = None
    ETA = serializers.JSONField(default='')

    class Meta:
        model = Restaurant
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Get the request object from the context
        request = self.context.get('request')
        
        # Get the value of the "extra_param" query parameter
        user_lat = request.query_params.get('latitude')
        user_lng = request.query_params.get('longitude')

        if user_lat and user_lng:
            origin = {
                'latitude': user_lat,
                'longitude': user_lng
            }

            ETA = getETA(origin=origin, dest=rep['location'])

            rep['ETA'] = ETA

        return rep

class UserRestaurantListSerializer(RestaurantProfileSerializer):
    cuisines = None
    
    class Meta:
        model = Restaurant
        fields = ('name', 'slug', 'specials', 'rating', 'image') 



    