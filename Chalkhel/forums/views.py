from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Profile, Post, Comment, Vote, Forum, ForumMember
from .forms import ProfileForm, PostForm, CommentForm, VoteForm, ForumForm, ForumMemberForm
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from django.contrib.auth import login, models
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import render


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ProfileListView(ListView):
    model = Profile


class ProfileDetailView(DetailView):
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm


class PostListView(ListView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm


class CommentListView(ListView):
    model = Comment


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm


class CommentDetailView(DetailView):
    model = Comment


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm


class VoteListView(ListView):
    model = Vote


class VoteCreateView(CreateView):
    model = Vote
    form_class = VoteForm


class VoteDetailView(DetailView):
    model = Vote


class VoteUpdateView(UpdateView):
    model = Vote
    form_class = VoteForm


class ForumListView(ListView):
    model = Forum


class ForumCreateView(CreateView):
    model = Forum
    form_class = ForumForm


class ForumDetailView(DetailView):
    model = Forum


class ForumUpdateView(UpdateView):
    model = Forum
    form_class = ForumForm


class ForumMemberListView(ListView):
    model = ForumMember


class ForumMemberCreateView(CreateView):
    model = ForumMember
    form_class = ForumMemberForm


class ForumMemberDetailView(DetailView):
    model = ForumMember


class ForumMemberUpdateView(UpdateView):
    model = ForumMember
    form_class = ForumMemberForm


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
