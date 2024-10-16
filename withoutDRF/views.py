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

        # Check for existing user with the same username or email
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        try:
            user = CustomUser(
                username=username, email=email, password=password, bio=bio
            )
            user.save()
            user.generate_token()  # Generate token on registration

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

                user.generate_token()

                return JsonResponse(
                    {
                        "message": "Login successful",
                        "username": user.username,
                        "token": user.token,
                    },
                    status=200,
                )
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def trial(request):
    if request.method == "GET":
        token = request.META.get("HTTP_AUTHORIZATION")

        # Check if token is present
        if not token:
            return JsonResponse({"error": "No token provided"}, status=401)

        try:
            # Assuming the token is passed as "Token <token_value>"
            token_value = token.split()[1]
            user = CustomUser.objects.get(token=token_value)

            if user:
                return JsonResponse(
                    {"message": "Welcome to the protected trial page!"}, status=200
                )
        except (CustomUser.DoesNotExist, IndexError):
            return JsonResponse({"error": "Invalid token"}, status=401)

    return JsonResponse({"error": "Method not allowed"}, status=405)
