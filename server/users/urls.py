from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = "users"

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", obtain_auth_token, name="login"),
]
