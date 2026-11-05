from django.contrib import admin
from .models import Team, TeamMembership, TeamSlugRedirect

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "acronym", "leader")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "role_in_team", "is_active")

@admin.register(TeamSlugRedirect)
class TeamSlugRedirectAdmin(admin.ModelAdmin):
    list_display = ("old_slug", "team")
