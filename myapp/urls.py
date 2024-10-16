# myapp/urls.py

from django.http import JsonResponse
from django.urls import path
from . import views

urlpatterns = [
    path("", views.default, name="index"),  # root URL for /myapp
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("trial/", views.trial, name="trial"),  # Protected route

    
    # path("", views.default, name="index"),
    # path("register/", views.register, name="register"),
    # path("login/", views.login, name="login"),
    # path("trial/", views.trial, name="trial"),  # Protected route
]
