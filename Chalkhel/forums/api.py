from . import models
from . import serializers
from rest_framework import viewsets, permissions, status
from . import permissionsmanager as p
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for the Profile class"""

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [p.IsOwnerOrReadOnly]

    @action(
        methods=['GET', 'PUT', 'PATCH', 'HEAD', 'OPTIONS'], detail=False,
        url_path='myprofile', permission_classes=[permissions.IsAuthenticated]
        )
    def show_my_profile(self, request):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            profile = request.user.profiles
            return Response({
                "user": serializers.ProfileSerializer(profile, context=self.get_serializer_context()).data,
            })
        elif request.method in ['PUT', 'PATCH']:
            profile = serializers.EventSerializer(data=request.data)
            if profile.is_valid():
                profile.save(user=self.request.user)
                return Response({
                    "user": serializers.ProfileSerializer(profile, context=self.get_serializer_context()).data,
                })
            return Response(data=profile.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='Method \"POST\" not allowed.')


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for the Post class"""

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [p.IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['GET', 'HEAD', 'OPTIONS'], detail=False,
            permission_classes=[permissions.IsAuthenticated], url_path='myposts')
    def my_posts_list(self, request):
        posts = request.user.posts.all()
        serializer = serializers.PostSerializer(posts, many=True)
        return Response({
            "posts": serializer.data
        })
        pass

    @action(methods=['GET', 'HEAD', 'OPTIONS'], detail=False,
            permission_classes=[permissions.IsAuthenticated], url_path='votedposts')
    def voted_post_list(self, request):
        posts = []
        votes = request.user.votes.all()
        for vote in votes:
            posts.append(vote.post)

        serializer = serializers.PostSerializer(posts, many=True)

        return Response({
            "posts": serializer.data
        })
        pass

    @action(methods=['get'], detail=True, permission_classes=[],
        url_path='comments')
    def post_comments(self, request, pk=None):
        post = get_object_or_404(models.Post, pk=pk)
        serializer = serializers.CommentSerializer(post.comments.all(), many=True)
        return Response({
            "comments": serializer.data,
        })


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Comment class"""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [p.IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['GET', 'HEAD', 'OPTIONS'], detail=False,
            permission_classes=[permissions.IsAuthenticated], url_path='mycomments')
    def my_comments_list(self, request):
        comments = request.user.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response({
            "comments": serializer.data
        })

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    """ViewSet for the Vote class"""

    queryset = models.Vote.objects.all()
    serializer_class = serializers.VoteSerializer
    permission_classes = [p.IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ForumViewSet(viewsets.ModelViewSet):
    """ViewSet for the Forum class"""

    queryset = models.Forum.objects.all()
    serializer_class = serializers.ForumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, p.IsOwnerOrReadOnly, p.SufficientPrestigeOrCantCreate]

    @action(methods=['get'], detail=True, permission_classes=[],
        url_path='members')
    def forum_members(self, request, pk=None):
        forum = get_object_or_404(models.Forum, pk=pk)
        serializer = serializers.UserSerializer(forum.members(), many=True)
        return Response({
            "members": serializer.data,
        })

    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated],
        url_path='myforums')
    def my_forums(self, request):
        forums = request.user.forums
        serializer = serializers.ForumSerializer(forums, many=True)
        return Response({
            "forums": serializer.data,
        })

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ForumMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for the ForumMember class"""

    queryset = models.ForumMember.objects.all()
    serializer_class = serializers.ForumMemberSerializer
    permission_classes = [p.IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)
