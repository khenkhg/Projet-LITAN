from django.contrib import admin
from .models import MemberWork

@admin.register(MemberWork)
class MemberWorkAdmin(admin.ModelAdmin):
    list_display = ("member", "category", "title", "status", "visibility")
    list_filter = ("category", "status", "visibility")
