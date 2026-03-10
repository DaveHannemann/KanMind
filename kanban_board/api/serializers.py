from rest_framework import serializers
from kanban_board.models import Board
from django.contrib.auth.models import User
from kanban_tasks.api.serializers import BoardTaskSerializer, UserShortSerializer

class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    member_count = serializers.SerializerMethodField()

    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]

    def get_member_count(self, obj):
        return obj.members.count()


class BoardCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    def create(self, validated_data):
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

    owner = UserShortSerializer(read_only=True)
    members = UserShortSerializer(many=True, read_only=True)
    tasks = BoardTaskSerializer(many=True, read_only=True)

    member_ids = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    many=True,
    write_only=True,
    required=False
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner",
            "members",
            "member_ids",
            "tasks",
        ]

    def update(self, instance, validated_data):
        member_ids = validated_data.pop("member_ids", None)

        if member_ids is not None:
            instance.members.set(member_ids)
            instance.members.add(instance.owner)

        return super().update(instance, validated_data)