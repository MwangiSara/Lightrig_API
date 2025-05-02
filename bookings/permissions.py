from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj): # Checks permission on a specific object (
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For client model with user field
        if hasattr(obj, 'user') and obj.user:
            return obj.user == request.user
        
        return False
    
class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
        custom permission to only allow authorized users to view and edit and anyone to create 
    """
    def has_permission(self, request, view): #Checks permission before accessing the view (before even fetching any object).
        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated
    
