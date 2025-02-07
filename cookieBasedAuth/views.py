from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer

# Generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# User Login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            tokens = get_tokens_for_user(user)
            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=False, samesite="Lax")
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=False, samesite="Lax")
            return response
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Protected Route (Requires Authentication)
class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "Protected route accessed!", "user": request.user.username})

# Refresh Token
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access_token": access_token}, status=status.HTTP_200_OK)
            response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite="Lax")
            return response
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# Logout API
class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
