"""
Academic offers (stages, PFE, thèses, post-docs).

Status flow: DRAFT → PENDING_REVIEW → VALIDATED (or REJECTED)

Automatic expiration: filtered at QUERY level (deadline >= today and
status = 'VALIDATED'). No cron job needed.

CASCADE replaced by:
  - supervisor: SET_NULL (offer survives if supervisor leaves)
  - team: PROTECT (a team with active offers cannot be deleted without
    reassigning them first — prevents silent orphaning of offers)
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class OfferType(models.TextChoices):
    STAGE = "stage", _("Stage")
    PFE = "pfe", _("PFE (Projet de Fin d'Études)")
    THESE = "these", _("Thèse de doctorat")
    POSTDOC = "postdoc", _("Post-doctorat")


class OfferStatus(models.TextChoices):
    DRAFT = "draft", _("Brouillon")
    PENDING_REVIEW = "pending_review", _("En attente de validation")
    VALIDATED = "validated", _("Validé et publié")
    REJECTED = "rejected", _("Rejeté")


class Offer(models.Model):
    title = models.CharField(max_length=300, verbose_name=_("Titre"))
    offer_type = models.CharField(
        max_length=10,
        choices=OfferType.choices,
        verbose_name=_("Type d'offre"),
        db_index=True,
    )
    description = models.TextField(verbose_name=_("Description"))
    requirements = models.TextField(
        blank=True, verbose_name=_("Prérequis")
    )

    # supervisor: SET_NULL — offer stays visible even if supervisor leaves
    supervisor = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="supervised_offers",
        verbose_name=_("Encadrant"),
    )
    # team: PROTECT — prevents accidental deletion of a team that has open offers
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.PROTECT,
        related_name="offers",
        verbose_name=_("Équipe"),
    )

    duration = models.CharField(
        max_length=100, blank=True, verbose_name=_("Durée"),
        help_text=_("Ex : 6 mois, 3 ans")
    )
    deadline = models.DateField(verbose_name=_("Date limite"), db_index=True)
    contact_email = models.EmailField(verbose_name=_("E-mail de contact"))

    status = models.CharField(
        max_length=15,
        choices=OfferStatus.choices,
        default=OfferStatus.DRAFT,
        verbose_name=_("Statut"),
        db_index=True,
    )
    # Validation audit trail
    validated_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="validated_offers",
        verbose_name=_("Validé par"),
    )
    validated_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Validé le")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("offre")
        verbose_name_plural = _("offres")
        ordering = ["deadline"]

    def __str__(self):
        return f"[{self.get_offer_type_display()}] {self.title}"
