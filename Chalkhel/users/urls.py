from knox import views as knox_views
from .views import RegisterAPI, LoginAPI, ProfileDetail, MyProfile
from .views import Website
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name="register"),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('api/myprofile/', MyProfile.as_view(), name='my-profile-detail'),
    path('api/profile/<str:pk>/', ProfileDetail.as_view(), name='profile-detail'),
# page view routes
    path('register', Website.register, name='register_page'),
    path('login', Website.login, name='login_page'),
]
