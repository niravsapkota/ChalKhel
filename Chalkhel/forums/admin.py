from django.contrib import admin
from .models import Forum, Post, ForumMember

# Register your models here.
@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'members', 'hidden')
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum', 'title', 'body', 'likes', 'dislikes', 'comments', 'hidden' )
    pass

@admin.register(ForumMember)
class ForumMemberAdmin(admin.ModelAdmin):
    list_display = ('forum', 'member')
    pass
