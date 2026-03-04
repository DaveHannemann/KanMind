from rest_framework.views import APIView
from rest_framework.response import Response
from kanban_board.models import Board
from kanban_board.api.serializers import BoardCreateSerializer, BoardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from kanban_board.api.permissions import IsBoardMember, IsBoardOwner

class BoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(members=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardCreateSerializer(
        data=request.data,
        context={"request": request}
    )

        serializer.is_valid(raise_exception=True)

        board = serializer.save()

        return Response(BoardSerializer(board).data, status=201)
    

class SingleBoardView(APIView):
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request, board_id):
        board = Board.objects.get(id=board_id)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def patch(self, request, board_id):
        board = Board.objects.get(id=board_id)

        serializer = BoardSerializer(
            board,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, board_id):

        if not IsBoardOwner().has_permission(request, self):
            return Response(
                {"detail": "Nur Besitzer darf löschen"},
                status=status.HTTP_403_FORBIDDEN
            )

        board = Board.objects.get(id=board_id)
        board.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)