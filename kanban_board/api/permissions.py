"""
Custom permission classes for board access control.
"""

from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    """
    Permission that allows access only to board members.
    """

    message = "403: Verboten. Der Benutzer muss Mitglied des Boards sein."

    def has_object_permission(self, request, view, obj):
        """
        Check whether the user is a member of the board.
        """

        return request.user in obj.members.all()


class IsBoardOwner(BasePermission):
    """
    Permission that allows access only to the board owner.
    """

    message = "403: Verboten. Nur der Eigentümer darf diese Aktion ausführen."

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is the owner of the board.
        """
        
        return obj.owner == request.user