from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class HasSpecialAccessPermission(permissions.BasePermission):
    """
    Custom permission to allow access to users with `has_special_access` set to True or if the user is an admin.
    """

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                (request.user.has_special_access or request.user.is_staff))



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (request.user and request.user.is_authenticated and
                request.user.has_special_access) or request.user.is_staff
        return request.user.is_staff



class IsAdminOrHasSpecialAccessOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it,
    and only allow admins or users with special access to view and modify all tasks.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            # Allow viewing if the user is admin or has special access
            if request.user.is_staff or request.user.has_special_access:
                return True
            # Otherwise, only allow if the object belongs to the user
            return obj.user == request.user

        # Write permissions are only allowed to admin users or those with special access
        return request.user.is_staff or request.user.has_special_access