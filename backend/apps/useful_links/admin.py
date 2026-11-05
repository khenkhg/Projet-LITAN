from django.contrib import admin
from .models import UsefulLink

@admin.register(UsefulLink)
class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_internal", "order")
    list_filter = ("category", "is_internal")
