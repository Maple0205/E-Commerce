from django.core.cache import cache
from django.core.mail import send_mail
import logging
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.views import APIView
from users.models import User
from carts.models import Cart
from carts.serializers import CartSerializer
from common.serializers import CustomResponse
from django.contrib.auth import logout, login
from drf_yasg.utils import swagger_auto_schema
from users.serializers import RegisterSerializer, VCodeSerializer, UserSerializer, ResetPasswordSerializer, EditUserSerializer, LoginSerializer, RefreshTokenSerializer, CustomTokenRefreshSerializer, UserProfileSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView

authentication_header = openapi.Parameter('Authorization', in_=openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING, required=True)

def generate_random_code(length=6):
    range_start = 10**(length-1)
    range_end = (10**length)-1
    return str(random.randint(range_start, range_end))

class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.pop('vcode')
            serializer.validated_data.pop('password_confirmation')
            serializer.validated_data['username'] = request.data.get('email')
            obj = User.objects.create_user(**serializer.validated_data)
            refresh = RefreshToken.for_user(obj)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            cart = Cart.objects.create(user=obj)
            res = {
                "username":obj.username,
                'id':obj.id,
                'email':obj.email,
                'token':access_token,
                'refresh':refresh_token,
                'cart': cart,
            }
            try:
                cart_serializer = CartSerializer(cart)
                res['cart'] = cart_serializer.data
            except Cart.DoesNotExist:
                res['cart'] = None
            data = CustomResponse.success(data=res)
            cache.delete(f'{obj.email}_verification_code')
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)

class SendCode(APIView):
    @swagger_auto_schema(request_body=VCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = VCodeSerializer(data=request.data)
        if serializer.is_valid():
            # username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            veri_code = generate_random_code()
            cache.set(f'maple_{email}_verification_code', veri_code, timeout=60)

            num_sent = send_mail(
                'EEshopping Center welcome you!',
                f'Hi {email}, your verification code is: {veri_code}',
                'info@eesupply.com.au',
                [email],
                fail_silently=False,
            )
            if num_sent:
                data = CustomResponse.success(data='Succeed! Code is: '+veri_code)
                return Response(data)
            else:
                data = CustomResponse.error(data='Failed!')
                return Response(data)
        else:
            return Response(serializer.errors, status=400)
        
class LoginView(TokenObtainPairView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = serializer.user
        result = serializer.validated_data
        response = Response()
        result['id'] = user.id
        result['phone'] = user.phone
        result['email'] = user.email
        result['username'] = user.username
        result['token'] = result.pop('access')
        try:
            cart = Cart.objects.get(user=user)
            cart_serializer = CartSerializer(cart)
            result['cart'] = cart_serializer.data
        except Cart.DoesNotExist:
            result['cart'] = None
        data = CustomResponse.success(data=result)
        response.data = data
        return response

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     @swagger_auto_schema(manual_parameters=[authentication_header])
#     def post(self, request):
#         logout(request)
#         data = CustomResponse.success(data='Logout successful')
#         return Response(data)

logger = logging.getLogger(__name__)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        logout(request)
        refresh_token = request.data.get('refresh')
        try:
            token = OutstandingToken.objects.get(token=refresh_token, blacklistedtoken__isnull=True)
            BlacklistedToken.objects.create(token=token)
        except OutstandingToken.DoesNotExist:
            logger.error(f'Token not found or already blacklisted: {refresh_token}')
        except Exception as e:
            logger.error(f'Error blacklisting token {refresh_token}: {str(e)}')
        
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class EditProfile(generics.UpdateAPIView):
    serializer_class = EditUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'options']

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=EditUserSerializer)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class ResetPassword(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'options']

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=ResetPasswordSerializer)
    def put(self, request, *args, **kwargs):
        user = request.user
        email = user.email
        serializer = ResetPasswordSerializer(data=request.data, context={'email': email})
        if serializer.is_valid():
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            data = CustomResponse.success(data="The password has been reset!")
            cache.delete(f'maple_{email}_verification_code')
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class GetUserProfile(APIView):
    # serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authentication_header], responses={200: UserProfileSerializer(many=False)})
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        data = CustomResponse.success(data=serializer.data)
        return Response(data, status=200)