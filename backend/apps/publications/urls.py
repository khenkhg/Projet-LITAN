from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"", views.PublicationViewSet, basename="publication")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/bibtex/", views.BibtexExportView.as_view(), name="publication-bibtex"),
    path("bibtex/", views.BibtexListExportView.as_view(), name="publication-bibtex-list"),
    path("doi-import/", views.DOIImportView.as_view(), name="publication-doi-import"),
]
