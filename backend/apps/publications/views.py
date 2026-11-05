# Placeholder — implemented in Milestone 1D
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Publication

class PublicationViewSet(ReadOnlyModelViewSet):
    queryset = Publication.objects.all()

class BibtexExportView(APIView):
    def get(self, request, pk):
        return Response({"detail": "Non implémenté."}, status=501)

class BibtexListExportView(APIView):
    def get(self, request):
        return Response({"detail": "Non implémenté."}, status=501)

class DOIImportView(APIView):
    def post(self, request):
        return Response({"detail": "Non implémenté."}, status=501)
