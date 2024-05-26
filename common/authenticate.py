from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import User
from rest_framework import serializers
class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
        except:
            raise serializers.ValidationError({'msg': "User doesn't exist!"})

        if user.check_password(password):
            return user
        else:
            raise serializers.ValidationError({'msg': "Password is not right!"})