from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT', 'DELETE']

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.created_by == request.user