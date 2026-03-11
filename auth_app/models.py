"""
Database models for the authentication system.
"""

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Extension of Django's default User model.

    This model stores additional information that is not included
    in Django's built-in User model.

    Fields:
        user (User):
            One-to-one relationship with Django's User model.

        fullname (str):
            Full name of the user.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    fullname = models.CharField(max_length=255)

    def __str__(self):
        """
        Return the username for readable representation.
        """
        
        return self.user.username