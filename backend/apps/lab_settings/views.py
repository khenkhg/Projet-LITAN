# Placeholder — implemented in Milestone 1E
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import LabSettings

class LabSettingsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        obj = LabSettings.get()
        return Response({"name": obj.name, "presentation": obj.presentation})
