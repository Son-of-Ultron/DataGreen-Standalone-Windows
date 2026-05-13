from rest_framework import permissions

from core.models import UserProfile


class IsDono(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == UserProfile.Role.DONO)
