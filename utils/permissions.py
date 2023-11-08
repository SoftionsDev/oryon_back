from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Implement the logic to check if the user is a system admin
        return request.user.groups.filter(name='admin').exists()


class IsManager(BasePermission):
    def has_permission(self, request, view):
        # Implement the logic to check if the user is a manager
        return request.user.groups.filter(name='manager').exists()


class IsCollaborator(BasePermission):
    def has_permission(self, request, view):
        # Implement the logic to check if the user is a collaborator
        return request.user.groups.filter(name='collaborator').exists()
