from django.contrib import admin
from .models import Publication, PublicationAuthor

class PublicationAuthorInline(admin.TabularInline):
    model = PublicationAuthor
    extra = 1
    ordering = ["order"]

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_type", "year", "doi")
    list_filter = ("publication_type", "year")
    search_fields = ("title", "doi")
    inlines = [PublicationAuthorInline]
