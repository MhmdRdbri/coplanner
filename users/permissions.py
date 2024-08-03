from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admin to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access any profile
        if request.user.is_staff:
            return True
        # User can access their own profile
        return obj.user == request.user