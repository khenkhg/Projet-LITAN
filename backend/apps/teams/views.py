# Placeholder — implemented in Milestone 1C
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team

class TeamViewSet(ReadOnlyModelViewSet):
    queryset = Team.objects.all()

class TeamSlugRedirectView(APIView):
    def get(self, request, old_slug):
        return Response({"detail": "Non implémenté."}, status=501)
