from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/teams/", include("apps.teams.urls")),
    path("api/publications/", include("apps.publications.urls")),
    path("api/works/", include("apps.works.urls")),
    path("api/news/", include("apps.news.urls")),
    path("api/equipment/", include("apps.equipment.urls")),
    path("api/offers/", include("apps.offers.urls")),
    path("api/useful-links/", include("apps.useful_links.urls")),
    path("api/lab-settings/", include("apps.lab_settings.urls")),
    # django-allauth social login endpoints
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
