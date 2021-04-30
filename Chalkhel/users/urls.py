from knox import views as knox_views
from .views import RegisterAPI
from .views import LoginAPI
from .views import ProfileAPI
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name="register"),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('api/profile/<user>', ProfileAPI.as_view(), name="profile" )
]
