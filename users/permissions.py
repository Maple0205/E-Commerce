from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user