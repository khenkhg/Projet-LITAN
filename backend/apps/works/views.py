# Placeholder — implemented in Milestone 1C
from rest_framework.viewsets import ModelViewSet
from .models import MemberWork

class MemberWorkViewSet(ModelViewSet):
    queryset = MemberWork.objects.none()
