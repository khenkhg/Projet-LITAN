from django.db import models
from django.utils.translation import gettext_lazy as _


class UsefulLink(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    url = models.URLField(verbose_name=_("URL"))
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Catégorie"),
        help_text=_("Ex : Bibliothèques en ligne, Organismes, Plateformes de publication"),
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    # False = visible to all visitors; True = logged-in members only
    is_internal = models.BooleanField(
        default=False,
        verbose_name=_("Membres seulement"),
        help_text=_("Si coché, ce lien n'est visible que par les membres connectés."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

    class Meta:
        verbose_name = _("lien utile")
        verbose_name_plural = _("liens utiles")
        ordering = ["category", "order", "title"]

    def __str__(self):
        return self.title
