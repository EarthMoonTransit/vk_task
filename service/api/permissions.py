from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'get_me', 'patch_me', 'delete_me']:
            return request.user.is_authenticated
        return (
                request.user.is_authenticated
                and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'get_me', 'patch_me', 'delete_me']:
            return request.user.is_authenticated
        return (
                request.user.is_authenticated
                and request.user.is_staff
        )