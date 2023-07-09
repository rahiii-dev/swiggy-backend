from django.http import Http404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from cart.models import CartModel, CartItemModel
from.models import Order, OrderItem
import order.constants as ord_const
from .serializers import OrderSerializer, OrderItemsSerializer, UserOrderSerializer, RestaurantOrderSerializer, DeliveryOrderSerializer

from restaurant.models import Restaurant
# Create your views here.
class OrderView(APIView):

    def get(self, request):
        userType = request.user.user_type

        # userType = 3
        # print(userType)

        if userType == 2: #user
            orders = Order.objects.filter(user=request.user)
            if orders:
                serializer = UserOrderSerializer(orders, many=True)
                return Response({'data': serializer.data})
        
        if userType == 3: #restaurant
            Filter = request.query_params.get('filter', None)
            rest = Restaurant.objects.filter(owner=request.user.pk).first()
            if rest:
                orders = Order.objects.filter(restaurant=rest.pk)

                if Filter == 'count':
                    count = orders.filter(order_status=ord_const.PENDING).count()
                    return Response(count)

                if orders:
                    serializer = RestaurantOrderSerializer(orders, many=True)
                    return Response({'data': serializer.data})
            
            if Filter == 'count':
                return Response(0)
        
        if userType == 4: #delivery
            orders = Order.objects.filter(Q(order_status=ord_const.CONFIRMED) | Q(order_status=ord_const.INDELIVERY))
            if orders:
                    serializer = DeliveryOrderSerializer(orders, many=True)
                    return Response({'data': serializer.data})

        return Response({'data': []})

    def post(self, request):
        cartId = request.data.get('cartID')
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')

        if cartId is None:
            return Response({'message': 'cartID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if lat is None:
            return Response({'message': 'latitude is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if lng is None:
            return Response({'message': 'longitude is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        lat = lat[:13]
        lng = lng[:13]

        cart = CartModel.objects.filter(pk=cartId).first()
        if cart:
            cartItems = CartItemModel.objects.filter(cart=cartId)
            order = Order.objects.create(user=request.user, restaurant=cart.restaurant,
                                         latitude=lat, longitude=lng )
            
            for item in cartItems:
                OrderItem.objects.create(order=order, cusine=item.cuisine, quantity=item.quantity)

            cart.delete()
            return Response({'message': 'Your order is succesfull.'})

        return Response({'message': 'Invalid cartID'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        userType = request.user.user_type

        orderId = request.data.get('orderID')
        if orderId is None:
            return Response({'message': 'orderID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.filter(pk=orderId)

        if order:
            Orderstatus = request.query_params.get('status', None)
            if Orderstatus:
                if Orderstatus == 'accept':
                    if userType == 3: #restaurant
                        order.update(order_status=ord_const.CONFIRMED)
                        return Response({'message': 'Order accepted.'})
                                        
                    if userType == 4: #delivery
                        order.update(order_status=ord_const.INDELIVERY)
                        return Response({'message': 'Order accepted.'})
                    
        
        return Response({'message': 'Invalid orderID'}, status=status.HTTP_400_BAD_REQUEST)
