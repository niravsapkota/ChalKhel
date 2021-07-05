from django.urls import path, include
from rest_framework import routers
from knox import views as knox_views

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'profile', api.ProfileViewSet)
router.register(r'post', api.PostViewSet)
router.register(r'comment', api.CommentViewSet)
router.register(r'vote', api.VoteViewSet)
router.register(r'forum', api.ForumViewSet)
router.register(r'forummember', api.ForumMemberViewSet)
router.register(r'notifications', api.NotificationViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for auth
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
)


urlpatterns += (
    # urls for Profile
    path('profile/', views.ProfileListView.as_view(), name='forums_profile_list'),
    # path('profile/create/', views.ProfileListView.as_view(), name='forums_profile_create'),
    path('profile/detail/<slug:slug>/', views.ProfileDetailView.as_view(), name='forums_profile_detail'),
    # path('profile/update/<slug:slug>/', views.ProfileUpdateView.as_view(), name='forums_profile_update'),


    #my-profile(api-done, regular remailing)
)

urlpatterns += (
    # urls for Post
    path('post/', views.PostListView.as_view(), name='forums_post_list'),
    path('post/create/', views.PostCreateView.as_view(), name='forums_post_create'),
    path('post/detail/<slug:slug>/', views.PostDetailView.as_view(), name='forums_post_detail'),
    path('post/update/<slug:slug>/', views.PostUpdateView.as_view(), name='forums_post_update'),

    #my-posts(api-done, regular remailing)
)

urlpatterns += (
    # urls for Comment
    path('comment/', views.CommentListView.as_view(), name='forums_comment_list'),
    path('comment/create/', views.CommentCreateView.as_view(), name='forums_comment_create'),
    path('comment/detail/<slug:slug>/', views.CommentDetailView.as_view(), name='forums_comment_detail'),
    path('comment/update/<slug:slug>/', views.CommentUpdateView.as_view(), name='forums_comment_update'),

    #my-comments
)

urlpatterns += (
    # urls for Vote
    path('vote/', views.VoteListView.as_view(), name='forums_vote_list'),
    path('vote/create/', views.VoteCreateView.as_view(), name='forums_vote_create'),
    # path('vote/detail/<int:pk>/', views.VoteDetailView.as_view(), name='forums_vote_detail'),
    path('vote/update/<int:pk>/', views.VoteUpdateView.as_view(), name='forums_vote_update'),

    #my-votes
    #like
    #dislike
    #unvote
)

urlpatterns += (
    # urls for Forum
    path('forum/', views.ForumListView.as_view(), name='forums_forum_list'),
    path('forum/create/', views.ForumCreateView.as_view(), name='forums_forum_create'),
    path('forum/detail/<slug:slug>/', views.ForumDetailView.as_view(), name='forums_forum_detail'),
    path('forum/update/<slug:slug>/', views.ForumUpdateView.as_view(), name='forums_forum_update'),


    #following-members
    #my-forums
)

urlpatterns += (
    # urls for ForumMember
    path('forummember/', views.ForumMemberListView.as_view(), name='forums_forummember_list'),
    path('forummember/create/', views.ForumMemberCreateView.as_view(), name='forums_forummember_create'),
    path('forummember/detail/<int:pk>/', views.ForumMemberDetailView.as_view(), name='forums_forummember_detail'),
    path('forummember/update/<int:pk>/', views.ForumMemberUpdateView.as_view(), name='forums_forummember_update'),

    #follow-Forum
    #unfollow-forum
)
