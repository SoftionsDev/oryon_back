from rest_framework.permissions import BasePermission


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        # Implement the logic to check if the user is a system admin
        pass


class IsManager(BasePermission):
    def has_permission(self, request, view):
        # Implement the logic to check if the user is a manager
        pass


class IsCommercial(BasePermission):
    def has_permission(self, request, view):
        # Implement the logic to check if the user is a commercial
        pass
