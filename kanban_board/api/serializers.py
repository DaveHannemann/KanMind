"""
Serializers for board related API responses.
"""

from rest_framework import serializers
from kanban_board.models import Board
from django.contrib.auth.models import User
from kanban_tasks.api.serializers import BoardTaskSerializer, UserShortSerializer

class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer used for the board list endpoint.

    Returns summary information about boards the user belongs to.

    Fields:
        id (int): Board identifier
        title (str): Board title
        member_count (int): Number of board members
        ticket_count (int): Total number of tasks
        tasks_to_do_count (int): Number of tasks with status "todo"
        tasks_high_prio_count (int): Number of tasks with high priority
        owner_id (int): ID of the board owner
    """

    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    member_count = serializers.SerializerMethodField()

    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]

    def get_member_count(self, obj):
        """
        Return number of members in the board.
        """

        return obj.members.count()


class BoardCreateSerializer(serializers.Serializer):
    """
    Serializer used to create a new board.

    Input:
        title (str): Name of the board
        members (list[int]): User IDs that should be members

    The requesting user automatically becomes the owner
    and is added as a member.
    """

    title = serializers.CharField()
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    def create(self, validated_data):
        """
        Create a board and assign members.

        Steps:
        1. Extract members
        2. Create board with current user as owner
        3. Assign members
        4. Ensure owner is always a member
        """

        members = validated_data.pop("members")
        owner = self.context["request"].user

        board = Board.objects.create(
            title=validated_data["title"],
            owner=owner
        )

        board.members.set(members)
        board.members.add(owner)

        return board


class SingleBoardSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single board.

    Includes:
        - owner information
        - board members
        - tasks belonging to the board
    """

    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    tasks = BoardTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        ]

    def to_representation(self, instance):
        """
        Override output for members 
        returns nested user data
        """
        representation = super().to_representation(instance)

        representation["members"] = UserShortSerializer(
            instance.members.all(), many=True
        ).data

        return representation

    def update(self, instance, validated_data):
        """
        Update board members.

        If members are provided:
        - update members list
        - ensure owner always remains a member
        """
        
        members = validated_data.pop("members", None)

        if members is not None:
            instance.members.set(members)
            instance.members.add(instance.owner)

        return super().update(instance, validated_data)
    
class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    owner_data = UserShortSerializer(source="owner", read_only=True)
    members_data = UserShortSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_data",
            "members_data",
        ]