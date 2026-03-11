"""
Serializers for comment API responses.
"""

from rest_framework import serializers
from kanban_comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for task comments.

    Returned fields:
        id (int): Comment identifier
        author (str): Full name of the comment author
        content (str): Comment text
        created_at (datetime): Creation timestamp
    """

    author = serializers.CharField(source="author.profile.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ["id", "created_at", "author"]

    def validate_content(self, value):
        """
        Ensure that comments are not empty or only whitespace.
        """
        
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value