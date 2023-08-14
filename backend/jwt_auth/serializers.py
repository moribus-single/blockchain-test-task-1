from rest_framework import serializers
from django.core.exceptions import BadRequest
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        if not password or not email:
            raise BadRequest("'email' and 'password' must be provided")
        
        # password validation
        try:
            validate_password(password, User)
        except:
            raise BadRequest("password is invalid")
        
        # hashing with default algorythm
        validated_data['password'] = make_password(password)
        return User.objects.create(**validated_data)


class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=128, required=False)

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            # validate the password
            try:
                validate_password(password, User)
            except:
                raise BadRequest("password is invalid")
            
            # hash the password
            instance.password = make_password(password)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance
    
class LoginOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ValidateOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
