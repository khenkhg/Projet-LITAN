"""
Publications, authors, and BibTeX generation.

Key design decisions (see docs/PROJECT_BRIEF.md):
  - bibtex_raw is NOT stored; BibTeX is generated on the fly from the
    structured fields to avoid stale data.
  - DOI is null (not empty string) when absent, so the unique constraint
    only applies to actual DOIs.
  - teams M2M is set at creation from the linked authors' current teams,
    so old publications are not affected when a member changes team later.
  - PublicationAuthor.member is nullable so external (non-lab) co-authors
    can still be listed by name.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class PublicationType(models.TextChoices):
    JOURNAL = "journal", _("Article de revue")
    CONFERENCE = "conference", _("Communication de conférence")
    BOOK_CHAPTER = "book_chapter", _("Chapitre d'ouvrage")
    THESIS = "thesis", _("Thèse / HDR")
    PATENT = "patent", _("Brevet")
    PREPRINT = "preprint", _("Prépublication")
    OTHER = "other", _("Autre")


class Publication(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Titre"))
    publication_type = models.CharField(
        max_length=20,
        choices=PublicationType.choices,
        default=PublicationType.JOURNAL,
        verbose_name=_("Type"),
    )
    year = models.PositiveIntegerField(verbose_name=_("Année"), db_index=True)
    publication_date = models.DateField(null=True, blank=True, verbose_name=_("Date de publication"))
    venue = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Revue / Conférence / Éditeur"),
    )
    volume = models.CharField(max_length=20, blank=True, verbose_name=_("Volume"))
    issue = models.CharField(max_length=20, blank=True, verbose_name=_("Numéro"))
    pages = models.CharField(max_length=30, blank=True, verbose_name=_("Pages"))

    # DOI: null (not blank string) when absent — unique constraint is safe
    doi = models.CharField(
        max_length=200,
        null=True,  # null = no DOI; unique enforced only on actual values
        blank=True,
        unique=True,
        verbose_name=_("DOI"),
    )
    url = models.URLField(blank=True, verbose_name=_("URL"))
    abstract = models.TextField(blank=True, verbose_name=_("Résumé"))

    # Teams snapshot: set at creation from authors' teams, never updated
    # automatically afterwards so old publications are unaffected by team changes.
    teams = models.ManyToManyField(
        "teams.Team",
        blank=True,
        related_name="publications",
        verbose_name=_("Équipes associées"),
        help_text=_(
            "Défini à la création à partir des équipes courantes des auteurs membres. "
            "Ne pas modifier manuellement sauf cas exceptionnel."
        ),
    )

    created_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_publications",
        verbose_name=_("Ajouté par"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("publication")
        verbose_name_plural = _("publications")
        ordering = ["-year", "title"]

    def __str__(self):
        return f"({self.year}) {self.title[:80]}"


class PublicationAuthor(models.Model):
    """
    Ordered list of authors for a publication.
    - author_name: always required (the name as it appears in the publication).
    - member: nullable FK linking to a lab member profile; null for external authors.
    """

    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="authors"
    )
    # Nullable: connects to lab member profile when the author is in the lab
    member = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="publication_authorships",
        verbose_name=_("Membre du labo"),
    )
    author_name = models.CharField(
        max_length=200,
        verbose_name=_("Nom de l'auteur"),
        help_text=_("Tel qu'il apparaît dans la publication."),
    )
    order = models.PositiveIntegerField(verbose_name=_("Ordre"))

    class Meta:
        verbose_name = _("auteur de publication")
        verbose_name_plural = _("auteurs de publications")
        unique_together = ("publication", "order")
        ordering = ["publication", "order"]

    def __str__(self):
        return f"{self.author_name} (ordre {self.order})"
