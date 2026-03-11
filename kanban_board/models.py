"""
Database model for the Kanban board system.
"""

from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    """
    Represents a Kanban board.

    Fields:
        title (str):
            Name of the board.

        owner (User):
            The user who created the board and has full control
            (including delete permissions).

        members (ManyToMany[User]):
            Users who have access to the board and its tasks.
            The owner is automatically included as a member.
    """

    title = models.CharField(max_length=255)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards"
    )

    members = models.ManyToManyField(
        User,
        related_name="member_boards"
    )

    def __str__(self):
        """
        Return the board title for readable representation.
        """
        
        return self.title