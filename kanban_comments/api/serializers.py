from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_comments.models import Comment
from kanban_tasks.api.serializers import UserShortSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.profile.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ["id", "created_at", "author"]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value