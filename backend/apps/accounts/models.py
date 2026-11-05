"""
accounts app — custom User model with:
- Status workflow: PENDING → APPROVED / REJECTED
- is_director and is_site_admin independent flags (no role enum)
- Team leader status derived from Team.leader FK (not stored here)
- MemberProfile with per-field visibility (Algerian Law 18-07)
- approved_by / approved_at audit trail
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def generate_profile_slug():
    return uuid.uuid4().hex[:12]


class VisibilityLevel(models.TextChoices):
    PUBLIC = "public", _("Public")
    INTERNAL = "internal", _("Membres connectés")
    PRIVATE = "private", _("Privé")


class MemberType(models.TextChoices):
    PERMANENT = "permanent", _("Permanent")
    ASSOCIATE = "associate", _("Associé")


class AccountStatus(models.TextChoices):
    PENDING = "pending", _("En attente d'approbation")
    APPROVED = "approved", _("Approuvé")
    REJECTED = "rejected", _("Rejeté")


class User(AbstractUser):
    """
    Custom user model. Username is kept for Django admin compatibility,
    but login is by email via Google OAuth.
    """

    # Email is the primary identifier — must be unique and lowercase
    email = models.EmailField(_("adresse e-mail"), unique=True)

    # Approval workflow
    status = models.CharField(
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING,
        db_index=True,
    )
    approved_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_users",
        verbose_name=_("Approuvé par"),
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Approuvé le"))

    # Membership type (null for director/admin who are not research members)
    member_type = models.CharField(
        max_length=10,
        choices=MemberType.choices,
        null=True,
        blank=True,
        verbose_name=_("Type de membre"),
    )

    # Independent privilege flags (not a role enum — a user can hold both)
    is_director = models.BooleanField(default=False, verbose_name=_("Directeur"))
    is_site_admin = models.BooleanField(default=False, verbose_name=_("Administrateur du site"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"

    @property
    def is_approved(self) -> bool:
        return self.status == AccountStatus.APPROVED

    @property
    def can_manage_site(self) -> bool:
        """True if the user is a director or site admin."""
        return self.is_director or self.is_site_admin

    def save(self, *args, **kwargs):
        # Normalize email to lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class MemberProfile(models.Model):
    """
    Extended profile for lab members. Each sensitive field has a companion
    *_visibility field (public / internal / private) to enforce Algerian
    Law 18-07 data privacy requirements.

    The API serializer MUST check the requesting user's role before
    including any non-PUBLIC field in the response.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", primary_key=True
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        default=generate_profile_slug,
        editable=False,
        verbose_name=_("Identifiant public URL"),
        help_text=_("Identifiant aléatoire unique non devinable pour les URLs publiques."),
    )

    # --- Photo ---
    photo = models.ImageField(
        upload_to="profiles/photos/", null=True, blank=True, verbose_name=_("Photo")
    )
    photo_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PUBLIC,
        verbose_name=_("Visibilité photo"),
    )

    # --- Bio ---
    bio = models.TextField(blank=True, verbose_name=_("Biographie"))
    bio_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PUBLIC,
        verbose_name=_("Visibilité bio"),
    )

    # --- Contact email (may differ from login email) ---
    contact_email = models.EmailField(blank=True, verbose_name=_("E-mail de contact"))
    email_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.INTERNAL,
        verbose_name=_("Visibilité e-mail"),
    )

    # --- Phone ---
    phone = models.CharField(
        max_length=30, blank=True, verbose_name=_("Téléphone")
    )
    phone_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PRIVATE,
        verbose_name=_("Visibilité téléphone"),
    )

    # --- Office ---
    office_location = models.CharField(
        max_length=100, blank=True, verbose_name=_("Bureau")
    )
    office_location_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.INTERNAL,
        verbose_name=_("Visibilité bureau"),
    )

    # --- Research ---
    research_domains = models.TextField(
        blank=True,
        verbose_name=_("Domaines de recherche"),
        help_text=_("Séparés par des virgules ou des sauts de ligne"),
    )
    research_domains_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PUBLIC,
        verbose_name=_("Visibilité domaines"),
    )

    # --- External links (always public unless overridden) ---
    orcid_id = models.CharField(
        max_length=20, blank=True, verbose_name=_("ORCID iD"),
        help_text=_("Format : 0000-0000-0000-0000"),
    )
    google_scholar_url = models.URLField(blank=True, verbose_name=_("Google Scholar"))
    researchgate_url = models.URLField(blank=True, verbose_name=_("ResearchGate"))
    linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn"))
    website_url = models.URLField(blank=True, verbose_name=_("Site personnel"))
    links_visibility = models.CharField(
        max_length=10,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PUBLIC,
        verbose_name=_("Visibilité liens"),
    )

    class Meta:
        verbose_name = _("profil de membre")
        verbose_name_plural = _("profils de membres")

    def __str__(self):
        return f"Profil de {self.user}"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_member_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.get_or_create(user=instance)
