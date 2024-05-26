# Maple
import re
from rest_framework import serializers
from users.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from typing import Any, Dict

if api_settings.BLACKLIST_AFTER_ROTATION:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8, max_length=16)
    password_confirmation = serializers.CharField(write_only=True, required=True, min_length=8, max_length=16)
    vcode = serializers.CharField(write_only=True, required=True, min_length=6, max_length=6)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation', 'vcode', 'suburb', 'address1', 'address2', 'state', 'phone', 'post_number', 'company_name', 'position', 'abn', 'acn', 'recipient_name')
    
    def validate_password(self, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, and one digit, with a minimum length of 8 characters and a maximum length of 16 characters.")
        return value
    
    def validate(self, attrs):
        vcode = attrs.get('vcode')
        email = attrs.get('email')
        vcode_cache = cache.get(f'maple_{email}_verification_code')
        if vcode != vcode_cache:
            raise ValidationError("Verification code is not right!")
        return attrs

class VCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=16)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=8, max_length=16)
    vcode = serializers.CharField(required=True, min_length=6, max_length=6)

    def validate_new_password(self, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\S]{8,16}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, and one digit, with a minimum length of 8 characters and a maximum length of 16 characters.")
        return value
    
    def validate(self, attrs):
        email = self.context.get('email')
        vcode = attrs.get('vcode')
        vcode_cache = cache.get(f'maple_{email}_verification_code')
        if vcode != vcode_cache:
            raise ValidationError("Verification code is not right!")
        return attrs
    
class EditUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    address1 = serializers.CharField(required=False)
    recipient_name = serializers.CharField(required=False)
    company_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('phone', 'post_number', 'state', 'suburb', 'address1', 'address2', 'recipient_name', 'abn', 'acn', 'company_name', 'industry', 'position', 'abn', 'acn')

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = self.token_class(attrs["refresh"])
        
        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

            from django.utils.timezone import now
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
            from rest_framework_simplejwt.utils import datetime_from_epoch

            user_id = refresh.payload['user_id']
            user = User.objects.get(pk=user_id)
            OutstandingToken.objects.create(
                user=user,
                jti=refresh.payload['jti'],
                token=str(refresh),
                created_at=now(),
                expires_at=datetime_from_epoch(refresh.payload['exp'])
            )
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserProfileSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('is_delete')
        self.fields.pop('password')