from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_tasks.models import Task

class UserShortSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(source="profile.fullname", read_only=True)

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
        read_only_fields = ["id", "board", "assignee", "reviewer", "comments_count"]

    def validate(self, data):
        board = self.context["board"]

        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({
                "assignee_id": "User must be a member of this board."
            })

        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({
                "reviewer_id": "User must be a member of this board."
            })

        return data

class BoardTaskSerializer(serializers.ModelSerializer):

    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()