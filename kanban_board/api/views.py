from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from kanban_board.models import Board
from kanban_board.api.serializers import BoardCreateSerializer, BoardSerializer, SingleBoardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from kanban_board.api.permissions import IsBoardMember, IsBoardOwner
from django.db.models import Count, Q

class BoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.annotate(
            ticket_count=Count("tasks", distinct=True),
            tasks_to_do_count=Count("tasks", filter=Q(tasks__status="todo"), distinct=True),
            tasks_high_prio_count=Count("tasks", filter=Q(tasks__priority="high"), distinct=True)
        )

    def get(self, request):
        boards = self.get_queryset().filter(members=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardCreateSerializer(
        data=request.data,
        context={"request": request}
    )

        serializer.is_valid(raise_exception=True)

        board = serializer.save()

        return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)
    

class SingleBoardView(APIView):

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsBoardOwner]
        else:
            permission_classes = [IsAuthenticated, IsBoardMember]
        return [permission() for permission in permission_classes]

    def get_object(self, board_id):
        return get_object_or_404(
        Board.objects.prefetch_related(
            "members",
            "tasks__assignee",
            "tasks__reviewer",
            "tasks__comments",
            ),
            id=board_id
        )

    def get(self, request, board_id):
        board = self.get_object(board_id)
        self.check_object_permissions(request, board)

        serializer = SingleBoardSerializer(board)
        return Response(serializer.data)

    def patch(self, request, board_id):
        board = self.get_object(board_id)
        self.check_object_permissions(request, board)

        serializer = SingleBoardSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, board_id):
        board = self.get_object(board_id)
        self.check_object_permissions(request, board)

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)