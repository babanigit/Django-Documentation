from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from .models import CustomUser


# Registration View
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        bio = data.get("bio", "")

        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)

        try:
            user = CustomUser(
                username=username, email=email, password=password, bio=bio
            )
            user.save()
            return JsonResponse({"username": user.username}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# Login View
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Both username and password are required"}, status=400
            )

        try:
            user = CustomUser.objects.get(username=username)
            if (
                user.password == password
            ):  # In a real app, never store passwords in plaintext!
                return JsonResponse(
                    {"message": "Login successful", "username": user.username},
                    status=200,
                )
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# Protected Trial View
@login_required  # This decorator ensures the user must be logged in
def trial(request):
    return JsonResponse({"message": "Welcome to the protected trial page!"})
