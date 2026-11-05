from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MemberProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "status", "is_director", "is_site_admin")
    list_filter = ("status", "is_director", "is_site_admin", "member_type")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("LITAN", {"fields": ("status", "member_type", "is_director", "is_site_admin", "approved_by", "approved_at")}),
    )


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_visibility", "email_visibility")
