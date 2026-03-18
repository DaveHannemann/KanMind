"""
Serializers for user authentication and registration.

This module contains serializers used for:
- returning user information
- registering new users
- logging in users
- validating email addresses
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning basic user information.

    Fields:
        id (int): Unique identifier of the user
        email (str): Email address of the user
        fullname (str): Full name stored in the UserProfile
    """
    user_id = serializers.IntegerField(source="id")
    fullname = serializers.CharField(source="profile.fullname")

    class Meta:
        model = User
        fields = ["user_id", "email", "fullname"]

class RegisterSerializer(serializers.Serializer):
    """
    Serializer used for registering a new user.

    Input fields:
        fullname (str): Full name of the user
        email (str): Email address (used as username)
        password (str): Password for the account
        repeated_password (str): Password confirmation

    After successful registration:
        - a new User object is created
        - a corresponding UserProfile is created
        - an authentication token is generated
    """

    fullname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the registration data.

        Checks:
        - Password and repeated_password must match
        - Email address must not already exist in the database

        Args:
            data (dict): Incoming serializer data

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If validation fails
        """

        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("User already exists")

        return data

    def create(self, validated_data):
        """
        Create a new user account.

        Steps:
        1. Remove repeated_password from validated data
        2. Create a new Django User
        3. Create a UserProfile linked to the user
        4. Generate an authentication token

        Args:
            validated_data (dict): Validated serializer data

        Returns:
            dict: Token and basic user information
        """

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
            "user_id": user.id,
        }


class LoginSerializer(serializers.Serializer):
    """
    Serializer used for authenticating users.

    Input fields:
        email (str): User email
        password (str): User password

    On successful authentication:
        - the user is authenticated via Django's authenticate()
        - a token is retrieved

    Returns:
        dict: Token and user information
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate login credentials.

        Uses Django's authenticate function to verify the user.

        Args:
            data (dict): Incoming login data

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If credentials are invalid
        """

        user = authenticate(
            username=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        self.user = user
        return data
    
    def create(self, validated_data):
        """
        Return authentication token for the user.

        If a token already exists it will be reused,
        otherwise a new token will be created.

        Args:
            validated_data (dict): Validated login data

        Returns:
            dict: Token and user information
        """
        user = self.user

        token, _ = Token.objects.get_or_create(user=user)

        return {
            "token": token.key,
            "fullname": user.profile.fullname,
            "user_id": user.id,
            "email": user.email,
        }

class EmailCheckSerializer(serializers.Serializer):
    """
    Serializer used to validate an email address.

    Fields:
        email (str): Email address to validate
    """
    
    email = serializers.EmailField(required=True)
    def validate(self, data):
        try:
            self.user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        return data
    
    def to_representation(self, instance):
        return {
            "id": self.user.id,
            "email": self.user.email,
            "fullname": self.user.profile.fullname,
        }