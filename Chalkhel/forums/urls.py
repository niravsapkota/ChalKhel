from .views import ForumDetail, PostDetail, ForumCreate, PostCreate, ForumMemberCreate, ForumMemberDelete
from django.urls import path

urlpatterns = [
path('api/forum/<str:pk>/', ForumDetail.as_view(), name="forum-detail"),
path('api/forum/', ForumCreate.as_view(), name="forum-create"),
path('api/post/<str:pk>/', PostDetail.as_view(), name="post-detail"),
path('api/forum/<str:forum>/post/', PostCreate.as_view(), name="post-create"),

path('api/forum/<str:forum>/follow/', ForumMemberCreate.as_view(), name="forummember-create"),
path('api/forum/<str:forum>/unfollow/', ForumMemberDelete.as_view(), name="forummember-delete"),

]
