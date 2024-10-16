from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from django.http import HttpResponse
import logging
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)


@api_view(["POST"])
def register(request):
    logger.info("Register view called")
    print("register view called")

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = serializer.save()
            logger.info(f"User {user.username} registered successfully")
            return Response({"username": user.username}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error saving user: {str(e)}")
            return Response(
                {"error": "Error creating user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    logger.warning(f"Invalid registration data: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    logger.info("Login view called")
    print("login view called")

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        logger.warning("Login attempt with missing credentials")
        return Response(
            {"error": "Both username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        logger.info(f"User {username} logged in successfully")
        return Response({"username": user.username}, status=status.HTTP_200_OK)

    logger.warning(f"Failed login attempt for user {username}")
    return Response(
        {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["GET"])
def default(request):
    logger.info("Default view called")
    return HttpResponse("Hello, this is the index page of myapp!")


@api_view(["GET"])
@permission_classes(
    [IsAuthenticated]
)  # Require authentication to access the trial route
def trial(request):
    return Response(
        {"message": "hello trail"},
        status=status.HTTP_200_OK,
    )
