from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import SignupSerializer
from rest_framework.authtoken.models import Token

# Create your views here.


class SignUp(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["success"] = True
            data["error"] = {}
            data["response"] = "Successfully registered"
            data["token"] = Token.objects.get(user=user).key
        else:
            data["success"] = False
            data["error"] = serializer.errors
        return JsonResponse(data)
