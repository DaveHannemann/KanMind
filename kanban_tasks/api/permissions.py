from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    message = "403: Verboten. Der Benutzer muss Mitglied des Boards sein."

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsBoardOwner(BasePermission):
    message = "403: Verboten. Nur der Eigentümer darf diese Aktion ausführen."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user