# Placeholder — implemented in Milestone 1E
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Equipment

class EquipmentViewSet(ReadOnlyModelViewSet):
    queryset = Equipment.objects.filter(is_operational=True)
