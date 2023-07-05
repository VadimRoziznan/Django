from rest_framework.permissions import BasePermission


class IsOwnerOrheadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in ["GET", "POST"]:
            return True
        return request.user == obj.creator
