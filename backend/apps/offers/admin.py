from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "offer_type", "team", "supervisor", "deadline", "status")
    list_filter = ("offer_type", "status", "team")
