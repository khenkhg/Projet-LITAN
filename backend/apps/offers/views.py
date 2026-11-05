# Placeholder — implemented in Milestone 1E
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Offer

class OfferViewSet(ReadOnlyModelViewSet):
    queryset = Offer.objects.none()
