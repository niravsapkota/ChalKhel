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


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns = (
    # urls for Django Rest Framework API
    path('', views.landing, name='landing'),
)

urlpatterns += (
    # urls for auth
    # path('register/', views.RegisterAPI.as_view(), name='register'),
    # path('login/', views.LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LoginView.as_view(), name='logout'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
)


urlpatterns += (
    # urls for Profile
    # path('profile/', views.ProfileCreateView.as_view(), name='forums_profile_create'),
    path('profile/', views.ProfileListView.as_view(), name='forums_profile_list'),

    path('profile/myprofile', views.MyProfile.posts, name='my-profile'),
    path('profile/myprofile/comments', views.MyProfile.comments, name='my-profile-comments'),
    path('profile/myprofile/votes', views.MyProfile.voted_posts, name='my-profile-voted-posts'),
    path('profile/myprofile/hidden', views.MyProfile.hidden_posts, name='my-profile-hidden-posts'),
    path('profile/myprofile/settings', views.MyProfile.settings, name='my-profile-settings'),

    path('profile/detail/<slug:slug>/', views.ProfileDetailView.posts, name='forums_profile_detail'),
    path('profile/detail/<slug:slug>/comments', views.ProfileDetailView.comments, name='forums_profile_comments'),

    path('profile/update/<slug:slug>/', views.ProfileUpdateView.as_view(), name='forums_profile_update'),


    #my-profile(api-done, regular remailing)
)

urlpatterns += (
    # urls for Post
    path('post/', views.PostListView.as_view(), name='forums_post_list'),
    path('<slug:slug>/post/create/', views.PostCreateView.as_view(), name='forums_post_create'),
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
    path('post/vote/create/', views.PostVoteCreateView.as_view(), name='forums_post_vote_create'),
    path('vote/detail/<int:pk>/', views.VoteDetailView.as_view(), name='forums_vote_detail'),
    path('vote/update/<int:pk>/', views.VoteUpdateView.as_view(), name='forums_vote_update'),
    path('vote/delete/<int:pk>/', views.VoteDeleteView.as_view(), name='forums_vote_delete'),

    path('comment/vote/create/', views.CommentVoteCreateView.as_view(), name='forums_comment_vote_create'),
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
    path('forummember/delete/<int:pk>/', views.ForumMemberDeleteView.as_view(), name='forums_forummember_delete'),

    #follow-Forum
    #unfollow-forum
)

urlpatterns += (
    # urls for ForumMember
    # path('forummember/', views.ForumMemberListView.as_view(), name='forums_forummember_list'),
    path('notifications/read', views.read_all_notifications, name='forums_notifications_update'),
    # path('forummember/delete/<int:pk>/', views.ForumMemberDeleteView.as_view(), name='forums_forummember_delete'),

    #follow-Forum
    #unfollow-forum
)
