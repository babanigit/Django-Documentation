# myapp/urls.py

from django.http import JsonResponse
from django.urls import path
from . import views

urlpatterns = [
    path("", views.default, name="index"),  # root URL for /myapp
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path(
        "trial/",
        lambda request: JsonResponse({"message": "Welcome to the trial page!"}),
        name="trial",
    ),
]
