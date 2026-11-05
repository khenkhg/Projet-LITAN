"""
Member works: projects, internships, supervisions.
(ARTICLE category removed per design decision — publications are shown
 automatically via PublicationAuthor. See docs/PROJECT_BRIEF.md.)
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import VisibilityLevel


class WorkCategory(models.TextChoices):
    PROJECT = "project", _("Projet de recherche")
    INTERNSHIP = "internship", _("Stage encadré")
    SUPERVISION = "supervision", _("Encadrement (thèse, PFE)")


class WorkStatus(models.TextChoices):
    ONGOING = "ongoing", _("En cours")
    COMPLETED = "completed", _("Terminé")


class MemberWork(models.Model):
    member = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="works",
        verbose_name=_("Membre"),
    )
    category = models.CharField(
        max_length=20,
        choices=WorkCategory.choices,
        verbose_name=_("Catégorie"),
    )
    title = models.CharField(max_length=300, verbose_name=_("Titre"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    role = models.CharField(
        max_length=100, blank=True, verbose_name=_("Rôle / Responsabilité")
    )
    status = models.CharField(
        max_length=10,
        choices=WorkStatus.choices,
        default=WorkStatus.ONGOING,
        verbose_name=_("Statut"),
    )
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Début"))
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Fin"),
        help_text=_("Laisser vide si en cours."),
    )
    institution_or_partner = models.CharField(
        max_length=200, blank=True, verbose_name=_("Institution / Partenaire")
    )
    include_in_cv = models.BooleanField(
        default=True, verbose_name=_("Inclure dans le CV")
    )
    visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PUBLIC,
        verbose_name=_("Visibilité"),
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage"),
        help_text=_("Les valeurs les plus basses apparaissent en premier."),
    )

    class Meta:
        verbose_name = _("travail")
        verbose_name_plural = _("travaux")
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.member} — {self.title[:60]}"
