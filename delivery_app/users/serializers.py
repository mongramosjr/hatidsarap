from rest_framework import serializers
from .models import HatidSarapUser, FaceImage, IDCardImage, VerificationRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HatidSarapUser
        fields = ('id', 'username', 'email', 'password', 'user_type', 'is_verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = HatidSarapUser.objects.create_user(**validated_data)
        return user


class FaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceImage
        fields = ('id', 'user', 'image', 'uploaded_at')


class IDCardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCardImage
        fields = ('id', 'user', 'image', 'uploaded_at')


class VerificationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = ('id', 'user', 'status', 'created_at', 'updated_at')