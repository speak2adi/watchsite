from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    # overriding has_permission model to allow only merchants
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_merchant
