from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# Create your views here.
from .models import Restaurant, RestaurantCuisines
from .serializers import RestaurantsRegisterSerializer, RestaurantProfileSerializer , CusineAddSerializer
from django.template.defaultfilters import slugify
import restaurant.constants as rest_const


from .serializers import UserRestaurantListSerializer, UserRestaurantViewSerializer, UserCuisineSerializer
class UserRestaurantView(APIView):
    permission_classes= [AllowAny]

    def get(self, request, slug=None):
        context = {
            'request': request
            }

        if slug:
            rest = Restaurant.objects.filter(slug=slug).first()
            if rest:
                serializer = UserRestaurantViewSerializer(rest, context=context)
                return Response(serializer.data)
        
        geoId = request.query_params.get('geoId', None)
        order_by = request.query_params.get('order', None)
        if geoId:
            rest = Restaurant.objects.filter(geofence_id=geoId)
            if rest:
                if order_by == 'rating':
                    rest = rest.order_by('-rating')

                serializer = UserRestaurantListSerializer(rest, many=True)
                return Response(serializer.data)
            
        return Response(False)
    
class UserCusinetView(APIView):
    permission_classes= [AllowAny]

    def get(self, request, slug=None):

        if slug:
            rest = Restaurant.objects.filter(slug=slug).first()
            if rest:
                cusines = RestaurantCuisines.objects.filter(restaurant=rest.pk)
                if cusines:
                    serializer = UserCuisineSerializer(cusines, many=True)
                    return Response({'cusines': serializer.data})
            
        return Response({'cusines': []})
        

class RestaurantFilterList(APIView):
   
   def get(self, request):
        queryset = Restaurant.objects.all()
        order_by = request.query_params.get('order', None)

        context = {
            'request': request
            }

        if order_by == 'rating':
            queryset = queryset.order_by('-rating')

        serializer = UserRestaurantListSerializer(queryset, many=True, context=context)
        return Response(serializer.data)
    

class RestaurantProfileView(APIView):

    def get(self, request):
        restaurant = Restaurant.objects.filter(owner=request.user.pk).first()
        if restaurant:
            serializer = RestaurantProfileSerializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(False)

class RestaurantRegisterView(APIView):

    def post(self, request):
        request.data['owner'] = request.user.pk

        if request.data['latitude'] and request.data['longitude']:
            request.data['latitude'] = request.data['latitude'][:13]
            request.data['longitude'] = request.data['longitude'][:13]
        
        if request.data['slug']:
            request.data['slug'] = slugify(request.data['slug'])
     
        serializer = RestaurantsRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            content = {
                'message' : 'Your Restaurant Added Succesfully'
            }
            return Response(content, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CuinineADD
from .models import RestaurantCuisines
from .serializers import RestaurantCuisineSerializer

class CuisineView(APIView):

    def get_object(self, pk):
        try:
            return RestaurantCuisines.objects.get(pk=pk)
        except RestaurantCuisines.DoesNotExist:
            raise Http404
            # return Response({'message': 'Cuisne not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        cuisine = self.get_object(id)
        serializer = RestaurantCuisineSerializer(cuisine)
        return Response(serializer.data)

    def post(self, request):
        restaurant = Restaurant.objects.filter(owner=request.user.pk).first()

        if not restaurant:
            return Response({'message': "You are not registered owner."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['restaurant'] = restaurant.id

        if request.data['cuisine_type']:
            for types in rest_const.CUISINE_TYPE_CHOICES:
                if request.data['cuisine_type'] in  types:
                    request.data['cuisine_type'] = types[0]
        
        serializer = CusineAddSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            content = {
                'message' : 'Your Cuisine Added Succesfully'
            }
            return Response(content, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        cuisine = self.get_object(id)

        if request.data['cuisine_type']:
            for types in rest_const.CUISINE_TYPE_CHOICES:
                if request.data['cuisine_type'] in  types:
                    request.data._mutable = True
                    request.data['cuisine_type'] = types[0]
                    request.data._mutable = False

        serializer = RestaurantCuisineSerializer(instance=cuisine, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            content = {
                'message' : 'Cuisine Updated Succesfully'
            }
            return Response(content, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        cuisine = self.get_object(id)
        cuisine.delete()
        return Response({"message": f'{cuisine.cuisine} deleted succesfully'})


#validators
class RestaurantValidator(APIView):

    def get(self, request, *args, **kwargs):

        Slug = request.query_params.get('slug', None)

        if Slug:
            Slug = slugify(Slug)
            if Restaurant.objects.filter(slug=Slug).exists():
                return Response(True)
            
        return Response(False)
        

# Zones
import requests
class ALLRestaurantZones(APIView):

    def get(self, req):
        url = 'https://api.radar.io/v1/geofences?tag=restaurant'
        headers = {
            'Authorization': 'prj_test_sk_7f18bfd0b153e1a0f99f422c6ef649dd729d4b41',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = {
                'geofences': response.json()['geofences']
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            print(response.json()['meta'])
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)