#accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        serializer = UserSerializer(user)
        first_name = serializer.data['first_name']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'first_name':first_name, 'username':username, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization').split()[1]
        if token:
            try:
                token_obj = Token.objects.get(key=token)
                user = token_obj.user
                first_name = user.first_name
                token_obj.delete()
                return Response({'message': f'Logout successful for user: {first_name}'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Token missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        
