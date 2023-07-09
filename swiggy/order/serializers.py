from rest_framework import serializers
from.models import Order, OrderItem
import order.constants as ord_const

from restaurant.models import Restaurant, RestaurantCuisines

class OrderItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderItem
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields='__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        OrderStatus = rep['order_status']

        for status in ord_const.ORDER_STATUS:
            if OrderStatus in status:
                rep['order_status'] = status[1]

        return rep

# User
class UserOrderItemsSerializer(OrderItemsSerializer):

    class Meta:
        model=OrderItem
        fields=('id', 'quantity', 'cusine')
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        cusine = RestaurantCuisines.objects.get(pk=rep['cusine'])
        
        rep['ordered_item'] = f"{rep['quantity']} x {cusine.cuisine}"
        return rep

class UserOrderSerializer(OrderSerializer):
    order = UserOrderItemsSerializer(read_only=True, many=True)

    class Meta:
        model=Order
        fields=('id', 'order', 'order_status', 'user', 'restaurant')
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rest = Restaurant.objects.get(pk=rep['restaurant'])
        rep['restaurant'] = rest.name

        return rep

# Restaurant
class RestaurantOrderSerializer(serializers.ModelSerializer):
    order = UserOrderItemsSerializer(read_only=True, many=True)

    class Meta:
        model=Order
        fields=('id', 'order', 'order_status', 'user')

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        OrderStatus = rep['order_status']

        if OrderStatus == 1:
            rep['order_acccepted'] = False
        else:
            rep['order_acccepted'] = True

        for status in ord_const.ORDER_STATUS:
            if OrderStatus in status:
                rep['order_status'] = status[1]

        return rep
    
class DeliveryOrderSerializer(serializers.ModelSerializer):
    order = UserOrderItemsSerializer(read_only=True, many=True)

    class Meta:
        model=Order
        fields=('id', 'order', 'order_status', 'user')

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        OrderStatus = rep['order_status']

        if OrderStatus == 2:
            rep['order_acccepted'] = False
        else:
            rep['order_acccepted'] = True

        for status in ord_const.ORDER_STATUS:
            if OrderStatus in status:
                rep['order_status'] = status[1]

        return rep
