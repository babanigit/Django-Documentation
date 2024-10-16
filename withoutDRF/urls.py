from django.urls import path

from . import views

app_name = "withoutDRF"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("trial/", views.trial, name="trial"),  # This route is now protected
]
