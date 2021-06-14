from django import forms
from .models import Profile, Post, Comment, Vote, Forum, ForumMember


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'prestige_points', 'avatar_hexcode', 'profile_pic', 'user']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name','hidden', 'media_content_type', 'media_content', 'likes', 'dislikes', 'comment_count', 'body', 'owner', 'forum']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'likes', 'dislikes', 'reply_count', 'owner', 'post']


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote_type', 'owner', 'post']


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'member_count', 'owner']


class ForumMemberForm(forms.ModelForm):
    class Meta:
        model = ForumMember
        fields = ['member', 'forum']
