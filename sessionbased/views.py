from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser
from django.contrib.auth.hashers import check_password


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
            user = CustomUser(username=username, email=email, bio=bio)
            user.set_password(password)  # Hash the password before saving
            user.save()
            user.generate_token()  # Generate token on registration

            return JsonResponse({"username": user.username}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


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

            # Check if the entered password matches the hashed password
            if check_password(password, user.password):
                # Log the user in (using session or token management)
                user.generate_token()  # Optionally generate a new token

                response = JsonResponse(
                    {
                        "message": "Login successful",
                        "username": user.username,
                    },
                    status=200,
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
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# Logout View
@csrf_exempt
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def trial(request):
    if request.method == "GET":
        # Get the token from the cookies
        token = request.COOKIES.get("auth_token")

        if not token:
            return JsonResponse({"error": "Authentication required"}, status=401)

        try:
            user = CustomUser.objects.get(token=token)
            if user:
                return JsonResponse(
                    {"message": "Welcome to the protected trial page!"}, status=200
                )
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "Invalid token"}, status=401)

    return JsonResponse({"error": "Method not allowed"}, status=405)
