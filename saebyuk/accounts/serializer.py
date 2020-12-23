from rest_framework import serializers
from .models import UserModel


class UserSerializer(serializers.Serializer):
    kakao_id = serializers.IntegerField()
    g_school_nickname = serializers.CharField(max_length=3)
    kakao_nickname = serializers.CharField(max_length=20)
    profile_image = serializers.CharField(max_length=20)
    is_manager = serializers.BooleanField()
