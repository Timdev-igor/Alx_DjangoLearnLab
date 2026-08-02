from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Anyone can read (list/retrieve products & categories).
    Only staff (is_staff_member or Django is_staff) can create/update/delete.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or getattr(request.user, "is_staff_member", False))
        )