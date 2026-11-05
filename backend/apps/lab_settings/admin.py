from django.contrib import admin
from .models import LabSettings

@admin.register(LabSettings)
class LabSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Singleton: prevent creation of a second record
        return not LabSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
