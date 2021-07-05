from . import models

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = (
            'id',
            'user',
            'slug',
            'created',
            'last_updated',
            'bio',
            'prestige_points',
            'avatar_hexcode',
            'profile_pic',
        )
        read_only_fields = ['id','user','slug', 'created', 'last_updated', 'prestige_points', 'avatar_hexcode']


class PostSerializer(serializers.ModelSerializer):
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Post
        fields = (
            'id',
            'forum',
            'owner',
            'slug',
            'hidden',
            'name',
            'created',
            'last_updated',
            'media_content_type',
            'media_content',
            'likes',
            'dislikes',
            'comment_count',
            'body',
        )
        read_only_fields = ['id', 'slug', 'owner','created', 'last_updated', 'likes', 'dislikes', 'comment_count']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'owner',
            'post',
            'slug',
            'created',
            'last_updated',
            'body',
            'likes',
            'dislikes',
            'reply_count',
        )
        read_only_fields = ['id','slug', 'created', 'owner', 'last_updated', 'likes', 'dislikes', 'reply_count']


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Vote
        fields = (
            'owner',
            'post',
            'pk',
            'created',
            'last_updated',
            'vote_type',
        )
        extra_kwargs = {'vote_type': {'required': True}}
        read_only_fields = ['created', 'last_updated','owner',]


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Forum
        fields = (
            'id',
            'owner',
            'slug',
            'name',
            'created',
            'last_updated',
            'member_count',
        )
        read_only_fields = ['slug', 'created','owner', 'last_updated', 'member_count']


class ForumMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ForumMember
        fields = (
            'pk',
            'member',
            'forum',
            'created',
            'last_updated',
        )
        read_only_fields = ['created','member', 'last_updated']

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = (
            'id',
            'sent_date',
            'read',
            'verb',
            'message',
            'sending_user',
            'post'
        )
        read_only_fields = ['id','sending_user','verb','sent_date', 'message','post']