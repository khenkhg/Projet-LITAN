"""
Custom allauth adapters for LITAN laboratory platform.

Security contract:
  1. Traditional password signup is disabled (LitanAccountAdapter).
  2. Only verified @estin.dz Google accounts are allowed (LitanSocialAccountAdapter).
  3. Domain is checked case-insensitively from token payload, not Google's 'hd' parameter.
  4. First login creates User with status=PENDING.
  5. Users with status=REJECTED are immediately denied login.
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import JsonResponse
from apps.accounts.models import AccountStatus, User

ALLOWED_DOMAIN = "estin.dz"


class LitanAccountAdapter(DefaultAccountAdapter):
    """
    Disable traditional password signup. Only Google OAuth is allowed.
    """

    def is_open_for_signup(self, request):
        return False


class LitanSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Restrict social login strictly to verified @estin.dz email addresses.
    """

    def is_open_for_signup(self, request, sociallogin):
        return True

    def pre_social_login(self, request, sociallogin):
        extra_data = sociallogin.account.extra_data or {}
        raw_email = extra_data.get("email") or ""
        email = raw_email.strip().lower()

        # 1. Require verified email
        is_verified = extra_data.get("email_verified")
        if is_verified is None:
            is_verified = extra_data.get("verified_email", False)

        if not is_verified:
            raise ImmediateHttpResponse(
                JsonResponse(
                    {"detail": "L'adresse e-mail Google doit être vérifiée."},
                    status=403,
                )
            )

        # 2. Server-side domain check (case-insensitive, independent of 'hd')
        if not email.endswith(f"@{ALLOWED_DOMAIN}"):
            raise ImmediateHttpResponse(
                JsonResponse(
                    {
                        "detail": (
                            f"Seules les adresses @{ALLOWED_DOMAIN} sont autorisées "
                            "sur cette plateforme."
                        )
                    },
                    status=403,
                )
            )

        # 3. Check if user already exists
        user = None
        if sociallogin.is_existing:
            user = sociallogin.user
        else:
            try:
                user = User.objects.get(email__iexact=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass

        # 4. Refuse rejected accounts
        if user and user.status == AccountStatus.REJECTED:
            raise ImmediateHttpResponse(
                JsonResponse(
                    {
                        "detail": (
                            "Votre demande d'accès a été rejetée par l'administration du laboratoire. "
                            "Contactez l'administration pour plus d'informations."
                        )
                    },
                    status=403,
                )
            )

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.status = AccountStatus.PENDING
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not user.status or user.status == AccountStatus.PENDING:
            user.status = AccountStatus.PENDING
            user.save(update_fields=["status"])
        return user
