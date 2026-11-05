from django.urls import path
from . import views

urlpatterns = [
    path("", views.LabSettingsView.as_view(), name="lab-settings"),
]
