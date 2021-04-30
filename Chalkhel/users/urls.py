from knox import views as knox_views
from .views import RegisterAPI
from .views import LoginAPI
from .views import Website
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name="register"),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('register', Website.register, name='register_page'),
    path('login', Website.login, name='login_page'),
]
