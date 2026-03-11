"""
Custom permissions for comment access control.
"""

from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    """
    Allows access only to members of a board.

    Works for:
    - Board objects
    - Task objects
    """

    message = "403: Verboten. Der Benutzer muss Mitglied des Boards sein."

    def has_object_permission(self, request, view, obj):
        """
        Determine the board from the object and check membership.
        """

        if hasattr(obj, "members"):
            board = obj

        elif hasattr(obj, "board"):
            board = obj.board

        else:
            return False

        return request.user in board.members.all() or request.user == board.owner


class IsCommentCreatorOrBoardOwner(BasePermission):
    """
    Permission allowing modification only by:

    - the comment author
    - the board owner
    """

    message = "403: Nur der Kommentar-Ersteller oder der Board-Owner darf diesen Kommentar löschen."

    def has_object_permission(self, request, view, obj):
        """
        Check whether the user is allowed to modify the comment.
        """
        
        return (
            obj.author == request.user or
            obj.task.board.owner == request.user
        )