from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

# Register
class UsercreationSerializer(serializers.ModelSerializer):     
    required_field_validation = ['userid', 'user_type', 'password']

    class Meta:
        model = CustomUser
        fields = ('user_type', 'userid', 'password',
                  'email', 'phone_no', 'full_name')
        
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, data):
        for field in self.required_field_validation:
            if field not in data:
                raise serializers.ValidationError(
                        {'message': f"{field} is required"})

        if 'email' in data and 'user_type' in data:
            if CustomUser.objects.filter(email=data['email'], user_type=data['user_type']).exists():
                raise serializers.ValidationError(
                    {'message': "This email is already in use"})
            
        if 'phone_no' in data and 'user_type' in data:
            if CustomUser.objects.filter(phone_no=data['phone_no'], user_type=data['user_type']).exists():
                raise serializers.ValidationError(
                    {'message': "This Phone Number is already in use"})

        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create(userid=validated_data['userid'], 
                                         user_type=validated_data['user_type'])
        
        user.set_password(validated_data['password'])

        if 'email' in validated_data:
            user.email = validated_data['email']
        if 'phone_no' in validated_data:
            user.phone_no = validated_data['phone_no']
        if 'full_name' in validated_data:
            user.full_name = validated_data['full_name']

        user.save()
        return user


# ViewUser
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('user_type', 'userid', 'full_name', 'email', 'phone_no')
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        try:
            value = rep.get('phone_no')
            if value:
                rep['phone_no'] = int(value)
        except ValueError:
            pass
        
        return rep

# Authenticate
class UserAuthSerializer(serializers.Serializer):
    userid = serializers.CharField(
        label="UserId",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        userid = attrs.get('userid')
        password = attrs.get('password')

        if userid and password:
            user = authenticate(userid=userid, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError({'message': msg})
            else:
                msg = 'Invalid UserId or Password.'
                raise serializers.ValidationError({'message': msg})
        else:
            msg = 'Must include "userid" and "password"'
            raise serializers.ValidationError({'message': msg})

        attrs['user'] = user
        return attrs