from rest_framework import generics,permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer


# <--------User Registration view---------------->
class RegisterView(generics.CreateAPIView):
    '''
    allow new users to register an account
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # save user
        user = serializer.save()

        # create token for user
        Token.objects.create(user=user)


# <--------------------User login view---------------->
class LoginView(ObtainAuthToken):
    '''returns user token wheb correct userame and password are provides
    '''
    def post(self,request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            "token": token.key,
            "username": token.user.username,
        })
    
# <---------------------Logout view----------------------->
class LogoutView(APIView):
    '''
    logs out user by deleting their token
    '''
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "message": "Logged out successfully."
        })