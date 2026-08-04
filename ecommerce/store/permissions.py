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

class IsOwner(permissions.BasePermission):
    """
    Object-level check: only the object's owner can access it.
    Used as a second layer, on top of IsAuthenticated.
    """
    def has_object_permission(self, request, view, obj):
        # works for objects with a direct `.user`, or via `.cart.user` / `.order.user`
        owner = getattr(obj, "user", None) or getattr(getattr(obj, "cart", None), "user", None)
        return owner == request.user