from django.shortcuts import render
from rest_framework.views import APIView
from main.tools import return_response, CacheMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
