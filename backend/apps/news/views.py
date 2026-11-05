# Placeholder — implemented in Milestone 1E
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import News

class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
