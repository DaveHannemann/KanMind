from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Task(models.Model):

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

    def __str__(self):
        return self.title