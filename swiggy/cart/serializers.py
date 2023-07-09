from .models import CartItemModel, CartModel
from restaurant.models import RestaurantCuisines, Restaurant
import restaurant.constants as rest_constants
from rest_framework import serializers


class CusinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCuisines
        fields = ('cuisine', 'price', 'cuisine_type')
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        CsnTypeValue = rep.get('cuisine_type')
        for cuisine in rest_constants.CUISINE_TYPE_CHOICES:
            if CsnTypeValue == cuisine[0]:
                rep['cuisine_type'] = cuisine[1]

        return rep

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('name',  'slug')




class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItemModel
        fields = '__all__'

class UserCartItemSerializer(CartItemSerializer):
    cuisine = CusinesSerializer(read_only=True)
    class Meta:
        model = CartItemModel
        exclude=['cart']

class CartSerializer(serializers.ModelSerializer):
    cart_items = UserCartItemSerializer(many=True, read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = CartModel
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        item_total = sum((float(item['cuisine']['price']) * item['quantity']) for item in rep['cart_items'])
        delivery_fee = 20

        rep['items_count'] = CartItemModel.objects.filter(cart=rep['id']).count()

        rep['item_total'] = item_total
        rep['delivery_fee'] = delivery_fee
        rep['cart_total'] = item_total + delivery_fee

        return rep


# from restaurant.models import RestaurantCuisines
class testCusineSerializer(serializers.ModelSerializer):
    pass

    # cart_details = serializers.SerializerMethodField('get_cart_details')

    # class Meta:
    #     model = RestaurantCuisines
    #     fields = '__all__'
    
    # def get_cart_details(self, obj):
    #     cart_items = CartItemModel.objects.filter(cuisine=obj)
    #     if cart_items.exists():
    #         cart_serializer = CartItemSerializer(cart_items, many=True)
    #         return cart_serializer.data
    #     return None
