from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_tasks.models import Task

class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskSerializer(serializers.ModelSerializer):

    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False
    )

    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "assignee_id",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]