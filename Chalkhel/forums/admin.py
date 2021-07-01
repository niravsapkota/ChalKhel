from django.contrib import admin
from django import forms
from .models import Profile, Post, Comment, Vote, Forum, ForumMember



'''Admin Features for <Profile>'''
class ProfileAdminForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ['slug', 'created', 'last_updated', 'bio', 'prestige_points', 'avatar_hexcode', 'profile_pic']
    readonly_fields = ['slug', 'created', 'last_updated', 'prestige_points', 'avatar_hexcode']


'''Admin Features for <Posts>'''
class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['name', 'slug','hidden', 'created', 'last_updated', 'media_content_type', 'media_content', 'likes', 'dislikes', 'comment_count', 'body']
    readonly_fields = ['slug', 'created', 'last_updated', 'likes', 'dislikes', 'comment_count']


'''Admin Features for <Comments>'''
class CommentAdminForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ['slug', 'created', 'last_updated', 'body', 'likes', 'dislikes', 'reply_count']
    readonly_fields = ['slug', 'created', 'last_updated', 'likes', 'dislikes', 'reply_count']


'''Admin Features for <Votes>'''
class VoteAdminForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = '__all__'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    form = VoteAdminForm
    list_display = ['owner', 'post', 'created', 'last_updated', 'vote_type']
    readonly_fields = ['created', 'last_updated']


'''Admin Features for <Forums>'''
class ForumAdminForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = '__all__'


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    form = ForumAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'member_count']
    readonly_fields = ['slug', 'created', 'last_updated', 'member_count']


'''Admin Features for <ForumMember>'''
class ForumMemberAdminForm(forms.ModelForm):

    class Meta:
        model = ForumMember
        fields = '__all__'


@admin.register(ForumMember)
class ForumMemberAdmin(admin.ModelAdmin):
    form = ForumMemberAdminForm
    list_display = ['created', 'last_updated']
    readonly_fields = ['created', 'last_updated']
