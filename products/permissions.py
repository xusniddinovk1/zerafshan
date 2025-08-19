from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user


class IsInstallmentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user
