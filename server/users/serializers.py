from rest_framework import serializers
from .models import User

# Define your serializers here


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["email"],
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user
