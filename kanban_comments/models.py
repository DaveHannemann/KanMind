from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):

    task = models.ForeignKey(
        "kanban_tasks.Task",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content