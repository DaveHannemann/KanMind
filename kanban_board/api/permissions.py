from rest_framework.permissions import BasePermission
from kanban_board.models import Board


class IsBoardMember(BasePermission):

    def has_permission(self, request, view):
        board_id = view.kwargs.get("board_id")

        if not board_id:
            return False

        return Board.objects.filter(
            id=board_id,
            members=request.user
        ).exists()
    

class IsBoardOwner(BasePermission):

    def has_permission(self, request, view):
        board_id = view.kwargs.get("board_id")

        if not board_id:
            return False

        return Board.objects.filter(
            id=board_id,
            owner=request.user
        ).exists()