from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Custom permission to check if the user is owner of the object. 
    """
    message = "You dont have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerOrReadOnly(BasePermission):
    """ check if the object blongs to request user.
    """
    message = "You dont have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method in SAFE_METHODS
