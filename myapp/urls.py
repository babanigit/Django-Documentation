# myapp/urls.py

from django.http import JsonResponse
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="RegisterView"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("trial/", views.TrialView.as_view(), name="trial"),  # Protected route
]
