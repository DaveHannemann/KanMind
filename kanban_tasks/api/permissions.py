"""
Custom permission classes for task access control.
"""

from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    """
    Allows access only to members of the board
    that the task belongs to.
    """

    message = "403: Verboten. Der Benutzer muss Mitglied des Boards sein."


    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "members"):
            return request.user in obj.members.all()

        if hasattr(obj, "board"):
            return request.user in obj.board.members.all()

        return False
class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Allows task deletion only for:

    - the task creator
    - the board owner
    """
    
    message = "403: Nur der Task-Ersteller oder der Board-Owner darf diese Task löschen."

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or obj.board.owner == request.user