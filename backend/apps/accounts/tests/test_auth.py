from importlib import import_module
import pytest
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.exceptions import ImmediateHttpResponse
from apps.accounts.models import User, MemberProfile, AccountStatus
from apps.accounts.adapters import LitanSocialAccountAdapter
from apps.teams.models import Team


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def adapter():
    return LitanSocialAccountAdapter()


def make_request(factory, path="/accounts/google/login/"):
    request = factory.get(path)
    engine = import_module(settings.SESSION_ENGINE)
    request.session = engine.SessionStore()
    return request


def make_social_login(email: str, verified: bool = True, user: User | None = None):
    """Helper to mock a Google SocialLogin object."""
    account = SocialAccount(
        provider="google",
        uid=f"google_{email}",
        extra_data={
            "email": email,
            "email_verified": verified,
            "name": "Test User",
            "given_name": "Test",
            "family_name": "User",
        },
    )
    if user:
        account.user = user
    else:
        user = User(email=email.lower(), username=email.lower())
    sociallogin = SocialLogin(account=account, user=user)
    return sociallogin


@pytest.mark.django_db
class TestGoogleDomainRestriction:
    def test_wrong_domain_rejected(self, factory, adapter):
        """Reject non-@estin.dz Google accounts."""
        request = make_request(factory)
        sociallogin = make_social_login("user@gmail.com")

        with pytest.raises(ImmediateHttpResponse) as exc:
            adapter.pre_social_login(request, sociallogin)

        response = exc.value.response
        assert response.status_code == 403
        assert b"@estin.dz" in response.content

    def test_unverified_email_rejected(self, factory, adapter):
        """Reject unverified email addresses even if domain is @estin.dz."""
        request = make_request(factory)
        sociallogin = make_social_login("hacker@estin.dz", verified=False)

        with pytest.raises(ImmediateHttpResponse) as exc:
            adapter.pre_social_login(request, sociallogin)

        response = exc.value.response
        assert response.status_code == 403

    def test_domain_is_case_insensitive(self, factory, adapter):
        """Domain check must be case-insensitive."""
        request = make_request(factory)
        sociallogin = make_social_login("Student.Name@ESTIN.DZ", verified=True)

        # Should not raise any exception
        adapter.pre_social_login(request, sociallogin)


@pytest.mark.django_db
class TestUserStatusFlow:
    def test_first_login_creates_pending_user(self, factory, adapter):
        """First login must create the user with status PENDING."""
        request = make_request(factory)
        sociallogin = make_social_login("newbie@estin.dz", verified=True)

        adapter.pre_social_login(request, sociallogin)
        user = adapter.save_user(request, sociallogin)

        assert user.pk is not None
        assert user.status == AccountStatus.PENDING
        assert not user.is_approved
        # MemberProfile must be created automatically with unique slug
        profile = MemberProfile.objects.get(user=user)
        assert len(profile.slug) > 0

    def test_rejected_user_refused_login(self, factory, adapter):
        """Users whose account was rejected must be denied login with 403."""
        rejected_user = User.objects.create(
            email="rejected@estin.dz",
            username="rejected@estin.dz",
            status=AccountStatus.REJECTED,
        )

        request = make_request(factory)
        sociallogin = make_social_login("rejected@estin.dz", verified=True, user=rejected_user)

        with pytest.raises(ImmediateHttpResponse) as exc:
            adapter.pre_social_login(request, sociallogin)

        response = exc.value.response
        assert response.status_code == 403
        assert b"rejet" in response.content.lower()

    def test_existing_approved_user_logs_in_normally(self, factory, adapter):
        """Approved users log in normally and keep their approved status."""
        approved_user = User.objects.create(
            email="approved@estin.dz",
            username="approved@estin.dz",
            status=AccountStatus.APPROVED,
        )

        request = make_request(factory)
        sociallogin = make_social_login("approved@estin.dz", verified=True, user=approved_user)

        # Should not raise exception
        adapter.pre_social_login(request, sociallogin)
        user = adapter.save_user(request, sociallogin)
        assert user.status == AccountStatus.APPROVED


@pytest.mark.django_db
class TestAuthMeEndpoint:
    def test_who_am_i_visitor(self, api_client):
        """Unauthenticated visitors get is_authenticated=False."""
        url = reverse("auth-me")
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["is_authenticated"] is False

    def test_who_am_i_authenticated_user_with_roles(self, api_client):
        """Authenticated user receives status and role flags."""
        user = User.objects.create(
            email="prof@estin.dz",
            username="prof@estin.dz",
            first_name="Karim",
            last_name="Bensaid",
            status=AccountStatus.APPROVED,
            is_director=True,
            is_site_admin=False,
        )
        # Create team led by user
        Team.objects.create(name="Systèmes Intelligents", slug="si", leader=user)

        api_client.force_login(user)
        url = reverse("auth-me")
        response = api_client.get(url)

        assert response.status_code == 200
        data = response.data
        assert data["is_authenticated"] is True
        assert data["email"] == "prof@estin.dz"
        assert data["status"] == "approved"
        assert data["is_approved"] is True
        assert data["is_director"] is True
        assert data["is_site_admin"] is False
        assert data["is_team_leader"] is True
        assert data["profile_slug"] is not None


@pytest.mark.django_db
class TestMemberAccessControl:
    def test_pending_user_blocked_from_member_endpoint(self, api_client):
        """Pending users cannot access member-only endpoints."""
        pending_user = User.objects.create(
            email="pending@estin.dz",
            username="pending@estin.dz",
            status=AccountStatus.PENDING,
        )
        api_client.force_login(pending_user)
        url = reverse("auth-member-check")
        response = api_client.get(url)
        assert response.status_code == 403

    def test_approved_user_allowed_member_endpoint(self, api_client):
        """Approved users can access member-only endpoints."""
        approved_user = User.objects.create(
            email="member@estin.dz",
            username="member@estin.dz",
            status=AccountStatus.APPROVED,
        )
        api_client.force_login(approved_user)
        url = reverse("auth-member-check")
        response = api_client.get(url)
        assert response.status_code == 200
