"""
Database model for Kanban tasks.
"""

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Represents a task within a Kanban board.

    A task belongs to a board and can be assigned to users
    for implementation and review.

    Fields:
        board (Board):
            The board this task belongs to.

        title (str):
            Short title describing the task.

        description (str):
            Detailed task description.

        status (str):
            Current workflow status of the task.

        priority (str):
            Importance level of the task.

        creator (User):
            User who created the task.

        assignee (User):
            User responsible for implementing the task.

        reviewer (User):
            User responsible for reviewing the task.

        due_date (date):
            Deadline for completing the task.
    """

    STATUS_CHOICES = [
        ("todo", "Todo"),
        ("in_progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
        
    board = models.ForeignKey(
        "kanban_board.Board",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)

    creator = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    related_name="created_tasks"
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_tasks"
    )

    due_date = models.DateField()

    class Meta:
        #Indexes to optimize queries filtering by board, assignee, and reviewer.
        indexes = [
            models.Index(fields=["board"]),
            models.Index(fields=["assignee"]),
            models.Index(fields=["reviewer"]),
        ]

    def __str__(self):
        """
        Return the task title for readable representation.
        """
        
        return self.title