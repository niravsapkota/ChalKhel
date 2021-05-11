from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from .models import Profile
from django.contrib.auth import login, models
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import render
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class Website():
    def register(request):
        return render(request, 'users/register.html')
    def login(request):
        return render(request, 'users/login.html')

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class ProfileDetail(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):

   queryset = Profile.objects.all()
   serializer_class = ProfileSerializer

   def get(self, request, *args, **kwargs):
       return self.retrieve(request, *args, **kwargs)

class MyProfile(generics.GenericAPIView):

   permission_classes = (permissions.IsAuthenticated,)
   queryset = Profile.objects.all()
   serializer_class = ProfileSerializer

   def get(self, request, *args, **kwargs):
       profile = self.queryset.get(user_id=self.request.user.id)
       return Response({
        "profile" : self.get_serializer(profile).data
       })

   def put(self, request, *args, **kwargs):
       serializer = self.get_serializer(self.queryset.get(user_id=self.request.user.id), data=request.data)
       serializer.is_valid(raise_exception=True)
       profile = serializer.save()
       return Response({
        "message": "The profile was updated successfully!",
        "profile": serializer.data
       })



# class ProfileView:
#
#     @api_view(['GET'])
#     def profileDetail(request, pk):
#         profile = Profile.objects.get(user=pk)
#         serializer = ProfileSerializer(profile, many=False)
#         return Response(serializer.data)
