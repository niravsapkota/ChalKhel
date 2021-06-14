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
        write_only = ['password']


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
        read_only_fields = ['id', 'slug', 'created', 'last_updated', 'likes', 'dislikes', 'comment_count']


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
        read_only_fields = ['id','slug', 'created', 'last_updated', 'likes', 'dislikes', 'reply_count']


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
        read_only_fields = ['created', 'last_updated']


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
        read_only_fields = ['slug', 'created', 'last_updated', 'member_count']


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
        read_only_fields = ['created', 'last_updated']
