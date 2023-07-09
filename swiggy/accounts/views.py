from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# Create your views here.
from .models import CustomUser
from .serializers import UserProfileSerializer, UsercreationSerializer, UserAuthSerializer
import accounts.constants as user_const

class UserProfile(APIView):

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        user = CustomUser.objects.get(userid=request.user)
        request.data._mutable = True
        request.data['userid'] = user.userid
        request.data._mutable = False

        if request.data['email'] != user.email:
            if CustomUser.objects.filter(email=request.data['email'], user_type=user.user_type).exists():
                return Response({'message': "This email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            
        if request.data['phone_no'] != user.phone_no:
            if CustomUser.objects.filter(phone_no=request.data['phone_no'], user_type=user.user_type).exists():
                return Response({'message': "This Phone Number is already in use"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(user, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

class UserList(APIView):

    def get(self, request):
        users = CustomUser.objects.exclude(user_type =user_const.ADMIN)
        serializer = UserProfileSerializer(users, many=True)

        return Response(serializer.data)

class UserCreate(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        if 'user_type' in request.data:
            for utype in user_const.USER_TYPE_CHOICES:
                if request.data['user_type'] in utype:
                    request.data._mutable = True
                    request.data['user_type'] = utype[0]
                    request.data._mutable = False

        user =  UsercreationSerializer(data=request.data)

        if user.is_valid():
            user.save()
            content = {
                'message': "User created Succesfully."
            }
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class UserLogin(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            content = {
                'token': token.key,
                'usertype': user.UserType
            }

            return Response(content)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# validation
class UserValidation(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        UserId = request.query_params.get('userid', None)
        PhoneNo = request.query_params.get('phone_no', None)
        Email = request.query_params.get('email', None)
        UserType = request.query_params.get('user_type', None)

        if UserId:
            if CustomUser.objects.filter(userid=UserId).exists():
                return Response(True)

        if UserType and UserType != 'admin':
            for utype in user_const.USER_TYPE_CHOICES:
                if UserType in utype:
                    UserType = utype[0]

        
        if PhoneNo and UserType:
            if CustomUser.objects.filter(phone_no=PhoneNo, user_type=UserType).exists():
                return Response(True)
                
        if Email and UserType:
            if CustomUser.objects.filter(email=Email, user_type=UserType).exists():
                return Response(True)
        
        return Response(False)

