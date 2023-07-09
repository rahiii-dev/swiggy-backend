from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import CartModel, CartItemModel
from .serializers import CartSerializer, CartItemSerializer, testCusineSerializer

from restaurant.models import RestaurantCuisines, Restaurant

class ChangeCart(APIView):
    def post(self, request):
        cartID = request.data.get('cartID')
        if cartID is None:
            return Response({'message': "cartID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = CartModel.objects.filter(pk=cartID).first()

        if cart:
            cartItems = CartItemModel.objects.filter(cart=cartID)

            userCart = CartModel.objects.filter(userid=request.user).first()
            if userCart:
                userCart.delete()
            
            newCart = CartModel.objects.create(userid=request.user, restaurant=cart.restaurant)

            for item in cartItems:
                CartItemModel.objects.create(cart=newCart, cuisine=item.cuisine, quantity=item.quantity)
            
            cart.delete()

            return Response({'message': "New cart created"})
        
        return Response({'message': "Invalid cartID"}, status=status.HTTP_400_BAD_REQUEST)




class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        userId = None
        if request.user.is_authenticated:
            userId = request.user.userid
        else:
            userId = request.query_params.get('guestId', None)
           
        if userId:
            cart = CartModel.objects.filter(userid=userId).first()

            if cart:
                serializer = CartSerializer(cart)
                return Response(serializer.data)
        
        return Response(None)
    
    def post(self, request):
        if request.user.is_authenticated:
            request.data._mutable = True
            request.data['userid'] = request.user.userid
            request.data._mutable = False

        cart, created = CartModel.objects.get_or_create(userid=request.data['userid'])
        restaurant = Restaurant.objects.get(pk=request.data['restaurant'])

        if (created == False) and cart.restaurant:
            if(cart.restaurant.pk != restaurant.pk):
                return Response({"message": f"You already have items of {cart.restaurant.name} restaurant."}, status=status.HTTP_400_BAD_REQUEST)
        
        if created == True:
            cart.restaurant = restaurant
            cart.save()
        
        cusine = RestaurantCuisines.objects.get(pk=request.data['cuisine'])
        cartItem, created = CartItemModel.objects.get_or_create(cart=cart, cuisine=cusine)
        if created:
            return Response({'message': "Item added to cart succesfully"})
        
        cartItem.quantity = cartItem.quantity + 1
        cartItem.save()
        return Response({'message': f"Item quantity increased to {cartItem.quantity}"})
    
    def put(self, request):
        try:
            alterType = request.data['type']
            cartItem = CartItemModel.objects.get(pk=request.data['itemId'])

            if alterType == 'increase':
                cartItem.quantity = cartItem.quantity + 1
                cartItem.save()
                return Response({'message': f"Item quantity increased to {cartItem.quantity}"})


            if alterType == 'decrease':
                cartItem.quantity = cartItem.quantity - 1
                if cartItem.quantity == 0:
                    cartItem.delete()

                    cartItems = CartItemModel.objects.filter(cart=cartItem.cart.id).count()
                    if(cartItems == 0):
                        cart = CartModel.objects.get(pk=cartItem.cart.id)
                        cart.delete()

                    return Response({'message': f"Item removed from cart"})
                
                cartItem.save()
                return Response({'message': f"Item quantity decreased to {cartItem.quantity}"})
            
        except Exception as e:
            return Response(None)

        


class CusineCartDetails(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id):

        userId = request.user

        if request.user.is_authenticated:
            userId = request.user.userid
        else:
            userId = request.query_params.get('guestId', None)
                    

        if userId:
            cusine = RestaurantCuisines.objects.filter(pk=id).first()

            if cusine:
                cart = CartModel.objects.filter(userid=userId).first()
                
                if cart:
                    cart_items = CartItemModel.objects.filter(cuisine=cusine, cart=cart.pk).first()
                    if cart_items:
                        cart_serializer = CartItemSerializer(cart_items)
                        return Response(cart_serializer.data)

        return Response(None)


class CartItemsCount(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        userId = request.user

        if request.user.is_authenticated:
            userId = request.user.userid
        else:
            userId = request.query_params.get('guestId', None)
                    
        if userId:
            cart = CartModel.objects.filter(userid=userId).first()

            if cart:
                cartitemsCount = CartItemModel.objects.filter(cart=cart.pk).count()
                return Response(cartitemsCount)
            
        return Response(0)