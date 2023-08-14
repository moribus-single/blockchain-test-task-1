from rest_framework import permissions

class IsAuthenticatedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        
        return obj == request.user