from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    message = "403: Verboten. Der Benutzer muss Mitglied des Boards sein."

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsTaskCreatorOrBoardOwner(BasePermission):
    message = "403: Nur der Task-Ersteller oder der Board-Owner darf diese Task löschen."

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or obj.board.owner == request.user