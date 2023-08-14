from django.contrib.auth.hashers import check_password
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timezone

from jwt_auth.permissions import IsAuthenticatedUser
from .utils import generate_otp
from .tasks import send_otp_email
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    LoginOTPSerializer,
    ValidateOTPSerializer,
)

class UserAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedUser, )

class UserAPICreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

class UserAPIUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticatedUser, )

class UserAPIDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedUser, )

class LoginOTPView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        # validation
        serializer = LoginOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "valid email and password must be provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.data
        email = validated_data['email']
        password = validated_data['password']
        
        # getting user object
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'user with this email does not exist'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not check_password(password, user.password):
            return Response(
                {'error': 'invalid password'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # generating otp code
        otp_code = generate_otp()
        user.otp = otp_code
        user.otp_set = datetime.now(tz=timezone.utc)
        print(f"otp_set = {user.otp_set}")
        user.save()

        # send otp code to the email
        send_otp_email.delay(email, otp_code)

        return Response({'ok': True})

class ValidateOTPView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        # validation
        serializer = ValidateOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'valid email and OTP code must be provided'})
        
        validated_data = serializer.data
        email = validated_data.get('email')
        otp = validated_data.get('otp')
        
        # getting user object
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'user with this email does not exist'})
        
        # validating otp in database
        if not user.otp:
            return Response({'error': 'user must authorize first'})
        
        if datetime.now(tz=timezone.utc) > user.otp_set + settings.OTP_LIFETIME:
            return Response({'error': 'OTP is expired'})
        
        # validating provided otp
        if otp != user.otp:
            return Response({'error': 'invalid OTP'})
        user.otp = ''
        user.save()
        
        # generating jwt tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
