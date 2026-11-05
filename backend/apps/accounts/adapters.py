"""
Social account adapter for django-allauth.

Security contract:
  1. Only @estin.dz emails are accepted.
  2. We verify the email domain on the SERVER from the OAuth token data,
     never from the Google "hd" hint parameter (which can be spoofed).
  3. First-time login creates the user with status=PENDING; the
     director/admin must approve before the user can access the members area.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import JsonResponse


ALLOWED_DOMAIN = "estin.dz"


class LitanSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Called after a successful OAuth exchange but before the user is
        connected/created. Reject any email not from @estin.dz.
        """
        email: str = sociallogin.account.extra_data.get("email", "")

        # Normalize and check domain — do NOT use sociallogin.account.extra_data["hd"]
        if not email.lower().endswith(f"@{ALLOWED_DOMAIN}"):
            raise ImmediateHttpResponse(
                JsonResponse(
                    {
                        "detail": (
                            "Seules les adresses @estin.dz sont autorisées "
                            "sur cette plateforme."
                        )
                    },
                    status=403,
                )
            )

    def save_user(self, request, sociallogin, form=None):
        """
        Override to set status=PENDING on first login (new user creation).
        Existing approved users keep their status.
        """
        user = super().save_user(request, sociallogin, form)
        # Only set PENDING if the user was just created (no previous status)
        from apps.accounts.models import AccountStatus
        if not user.pk or user.status == AccountStatus.PENDING:
            user.status = AccountStatus.PENDING
            user.save(update_fields=["status"])
        return user
