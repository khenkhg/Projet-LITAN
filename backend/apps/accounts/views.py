# Placeholder — views will be implemented in Milestone 1B
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User, MemberProfile


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"email": request.user.email, "status": request.user.status})
        return Response({"detail": "Non authentifié."}, status=401)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.none()


class MemberProfileViewSet(ModelViewSet):
    queryset = MemberProfile.objects.none()


class PendingAccountsView(APIView):
    def get(self, request):
        return Response([])


class ApproveAccountView(APIView):
    def post(self, request, pk):
        return Response({"detail": "Non implémenté."}, status=501)


class RejectAccountView(APIView):
    def post(self, request, pk):
        return Response({"detail": "Non implémenté."}, status=501)
