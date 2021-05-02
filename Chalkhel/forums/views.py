from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import ForumSerializer, PostSerializer
from .models import Forum, Post, ForumMember
from django.contrib.auth import login, models
from django.shortcuts import render

# Hidden content can only be seen by the owner (done)
# Contents can only be edited by the owners (done)


class ForumDetail(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):

    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def get(self, request, *args, **kwargs):
        forum_data = self.queryset.get(id=kwargs['pk'])
        if forum_data.hidden == False or forum_data.user.id == self.request.user.id:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({
            "message": "The user has hidden the contents of this forum!",
            })

    def put(self, request, *args, **kwargs):
        forum_data = self.queryset.get(id=kwargs['pk'])
        if forum_data.user == self.request.user:
            serializer = self.get_serializer(forum_data, data=request.data)
            serializer.is_valid(raise_exception=True)
            forum = serializer.save()
            return Response({
            "message": "The forum was updated successfully!",
            "forum": self.get_serializer(forum).data,
            })
        else:
            return Response({
            "message": "You don't have permission to edit this forum!"
            })


class ForumCreate(generics.GenericAPIView):

    serializer_class = ForumSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        forum = serializer.save(user=self.request.user )
        return Response({
        "message": "Forum created successfully!",
        "forum": self.get_serializer(forum).data,
        })


class PostDetail(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        post_data = self.queryset.get(id=kwargs['pk'])
        if post_data.hidden == False or post_data.user.id == self.request.user.id:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({
            "message": "The user has hidden the contents of this post!"
            })

    def put(self, request, *args, **kwargs):
        post_data = self.queryset.get(id=kwargs['pk'])
        if post_data.user == self.request.user:
            serializer = self.get_serializer(post_data, data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            return Response({
            "message": "The post was updated successfully!",
            "forum": self.get_serializer(post).data,
            })
        else:
            return Response({
            "message": "You don't have permission to edit this post!"
            })

class PostCreate(generics.GenericAPIView):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        forum = Forum.objects.get(id=kwargs['forum'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(user=self.request.user, forum=forum )
        return Response({
        "message": "Post created successfully!",
        "post": self.get_serializer(post).data,
        })

class ForumMemberCreate(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        forum = Forum.objects.get(id=kwargs['forum'])
        forumfollower = ForumMember(forum=forum,member=self.request.user)
        forumfollower.save()
        return Response({
        "message": "followed the forum successfully",
        })

class ForumMemberDelete(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        forum = Forum.objects.get(id=kwargs['forum'])
        forumfollower = ForumMember.objects.get(forum=forum,member=self.request.user)
        forumfollower.delete()
        return Response({
        "message": "unfollowed the forum successfully",
        })
