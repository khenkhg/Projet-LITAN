from rest_framework.permissions import BasePermission
from apps.accounts.models import AccountStatus


class IsApprovedMember(BasePermission):
    """
    Allows access only to authenticated users whose account has been approved.
    Pending or rejected users are denied access.
    """

    message = "Votre compte est en attente d'approbation ou inactif."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.status == AccountStatus.APPROVED
        )


class IsDirectorOrAdmin(BasePermission):
    """
    Allows access only to approved users who are either Director or Site Admin.
    """

    message = "Accès réservé à la direction et aux administrateurs."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.status == AccountStatus.APPROVED
            and (request.user.is_director or request.user.is_site_admin)
        )
