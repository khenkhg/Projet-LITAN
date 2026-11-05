"""
LabSettings — a singleton model (always pk=1).
Stores lab presentation, contact info, and other site-wide config.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class LabSettings(models.Model):
    name = models.CharField(
        max_length=200, default="Laboratoire LITAN", verbose_name=_("Nom du laboratoire")
    )
    presentation = models.TextField(
        blank=True,
        verbose_name=_("Présentation"),
        help_text=_("Texte affiché sur la page À propos / Accueil."),
    )
    contact_email = models.EmailField(blank=True, verbose_name=_("E-mail de contact"))
    contact_phone = models.CharField(
        max_length=30, blank=True, verbose_name=_("Téléphone")
    )
    address = models.TextField(blank=True, verbose_name=_("Adresse"))
    map_embed_url = models.URLField(
        blank=True, verbose_name=_("URL de carte intégrée (iframe)"),
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("paramètres du laboratoire")
        verbose_name_plural = _("paramètres du laboratoire")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Enforce singleton — always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls) -> "LabSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
