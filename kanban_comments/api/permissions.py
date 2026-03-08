from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    message = "403: Verboten. Der Benutzer muss Mitglied des Boards sein."

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "members"):
            board = obj

        elif hasattr(obj, "board"):
            board = obj.board

        else:
            return False

        return request.user in board.members.all() or request.user == board.owner


class IsCommentCreatorOrBoardOwner(BasePermission):
    message = "403: Nur der Kommentar-Ersteller oder der Board-Owner darf diesen Kommentar löschen."

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user or
            obj.task.board.owner == request.user
        )