from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .models import Forum, Post

class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = '__all__'
        read_only = ['user', 'members']

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only = ['user', 'forum', 'likes', 'dislikes', 'comments']
