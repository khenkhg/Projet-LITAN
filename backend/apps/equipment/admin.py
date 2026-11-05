from django.contrib import admin
from .models import Equipment, EquipmentPhoto

class EquipmentPhotoInline(admin.TabularInline):
    model = EquipmentPhoto
    extra = 1

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_operational")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [EquipmentPhotoInline]
