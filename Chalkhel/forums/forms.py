from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment, Vote, Forum, ForumMember


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields = ['name', 'hidden', 'media_content_type', 'media_content', 'likes', 'dislikes', 'comment_count', 'body', 'owner', 'forum']
        fields = ['name', 'hidden', 'media_content_type', 'media_content', 'body', 'forum']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        # fields = ['body', 'likes', 'dislikes', 'reply_count', 'owner', 'post']


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote_type']


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'bio', 'profile_pic', 'cover_pic']


class ForumMemberForm(forms.ModelForm):
    class Meta:
        model = ForumMember
        fields = ['member', 'forum']
        fields = ['member', 'forum']
        model = ForumMember
        fields = ['member', 'forum']
        fields = ['member', 'forum']
