from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE METHODS ARE GET, HEAD, OR OPTIONS request
        if request.method in permissions.SAFE_METHODS:
            return True
        # verify if the user trying to access is really the owner
        return obj.owner == request.user
