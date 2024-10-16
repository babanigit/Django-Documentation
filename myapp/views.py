# using DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        bio = data.get("bio", "")

        if not username or not email or not password:
            return Response(
                {"error": "All fields (username, email, password) are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for existing user with the same username or email
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser(username=username, email=email, bio=bio)
            user.set_password(password)  # Hash the password before saving
            user.save()
            user.generate_token()  # Generate token on registration

            return Response({"username": user.username}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"An error occurred during registration: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(username=username)

            # Check if the entered password matches the hashed password
            if check_password(password, user.password):
                user.generate_token()  # Optionally generate a new token

                response = Response(
                    {
                        "message": "Login successful",
                        "username": user.username,
                    },
                    status=status.HTTP_200_OK,
                )

                # Set the token in cookies
                response.set_cookie(
                    key="auth_token",
                    value=user.token,
                    httponly=True,  # Prevents JavaScript access to the cookie
                    secure=False,  # Set to True if you're using HTTPS
                    samesite="Lax",  # Prevents CSRF attacks to some extent
                )

                return response
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get("auth_token")
        if not token:
            return Response(
                {"error": "Authentication token not provided"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            user = CustomUser.objects.get(token=token)
            user.token = None  # Clear the token in the database
            user.save()
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid token, user not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("auth_token")  # Clear the token cookie
        return response


class TrialView(APIView):
    def get(self, request):
        # Get the token from the cookies
        token = request.COOKIES.get("auth_token")

        if not token:
            return Response(
                {"error": "Authentication required. Please login first."}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            user = CustomUser.objects.get(token=token)
            return Response(
                {"message": "Welcome to the protected trial page!"}, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token. Please login again."}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
