from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="profile.fullname")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

class RegisterSerializer(serializers.Serializer):

    fullname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("User already exists")

        return data

    def create(self, validated_data):
        validated_data.pop("repeated_password")

        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        UserProfile.objects.create(
            user=user,
            fullname=validated_data["fullname"]
        )

        token = Token.objects.create(user=user)

        return {
            "token": token.key,
            "fullname": user.profile.fullname,
            "email": user.email,
            "id": user.id,
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        self.user = user
        return data
    
    def create(self, validated_data):
        user = self.user

        token, _ = Token.objects.get_or_create(user=user)

        return {
            "token": token.key,
            "fullname": user.profile.fullname,
            "id": user.id,
            "email": user.email,
        }

class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)