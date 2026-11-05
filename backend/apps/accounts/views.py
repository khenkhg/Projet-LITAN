from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User, MemberProfile, AccountStatus
from .permissions import IsApprovedMember


class CurrentUserView(APIView):
    """
    Endpoint returning the current user's authentication and authorization state.
    Unauthenticated visitors receive is_authenticated: false without throwing 401.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "is_authenticated": False,
                    "status": None,
                    "detail": "Non authentifié.",
                }
            )

        # Check if user leads any team
        is_team_leader = user.led_teams.exists()
        profile_slug = None
        if hasattr(user, "profile") and user.profile:
            profile_slug = user.profile.slug

        return Response(
            {
                "is_authenticated": True,
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.get_full_name() or user.email,
                "status": user.status,
                "is_approved": user.is_approved,
                "is_director": user.is_director,
                "is_site_admin": user.is_site_admin,
                "is_team_leader": is_team_leader,
                "member_type": user.member_type,
                "profile_slug": profile_slug,
            }
        )


class LogoutView(APIView):
    """
    Terminates the session and logs the user out.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"detail": "Déconnexion réussie."})


class MemberAreaCheckView(APIView):
    """
    Endpoint strictly reserved for approved members.
    Used to test that pending and rejected accounts are denied access.
    """

    permission_classes = [IsApprovedMember]

    def get(self, request):
        return Response(
            {
                "detail": f"Accès autorisé pour le membre approuvé {request.user.email}.",
                "status": request.user.status,
            }
        )


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.filter(status=AccountStatus.APPROVED)


class MemberProfileViewSet(ModelViewSet):
    queryset = MemberProfile.objects.filter(user__status=AccountStatus.APPROVED)


class PendingAccountsView(APIView):
    def get(self, request):
        return Response([])


class ApproveAccountView(APIView):
    def post(self, request, pk):
        return Response({"detail": "Non implémenté."}, status=501)


class RejectAccountView(APIView):
    def post(self, request, pk):
        return Response({"detail": "Non implémenté."}, status=501)
