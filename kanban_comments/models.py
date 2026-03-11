"""
Database models for task comments.
"""

from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    """
    Represents a comment on a task.

    Fields:
        task (Task):
            The task this comment belongs to.

        author (User):
            The user who created the comment.

        content (str):
            Text content of the comment.

        created_at (datetime):
            Timestamp when the comment was created.
    """

    task = models.ForeignKey(
        "kanban_tasks.Task",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        """
        Return a shortened preview of the comment.
        """
        return self.content[:20] + "..."