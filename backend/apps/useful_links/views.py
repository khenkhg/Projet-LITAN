# Placeholder — implemented in Milestone 1E
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import UsefulLink

class UsefulLinkViewSet(ReadOnlyModelViewSet):
    queryset = UsefulLink.objects.filter(is_internal=False)
