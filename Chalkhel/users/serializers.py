from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .models import Profile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        write_only = ['password']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        read_only = ['prestige_points', 'read_only', 'user', 'avatar_hex']

    def get_username(self, obj):
        return obj.user.username

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance
