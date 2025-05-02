from rest_framework import permissions

class IsAuthenticatedOrViewOnly(permissions.BasePermission):
    """
        custom permission to only allow authorized users to edit and anyone to view 
    """
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user and request.user.is_authenticated