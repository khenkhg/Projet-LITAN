"""
Teams and memberships.

Access rules (enforced in views/serializers, not just the model):
  - Only can_manage_site (director or site admin) may create, rename,
    merge or delete teams.
  - A team leader may edit ONLY their own team's description and research_axes.
  - Team merge/rename: news, offers and memberships are reassigned to the
    target team. A TeamSlugRedirect record keeps old URLs alive.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_("Nom"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Slug URL"))
    acronym = models.CharField(
        max_length=20, unique=True, blank=True, verbose_name=_("Acronyme")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    research_axes = models.JSONField(
        default=list,
        verbose_name=_("Axes de recherche"),
        help_text=_("Liste de chaînes de caractères décrivant les axes de recherche."),
    )
    leader = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="led_teams",
        verbose_name=_("Responsable d'équipe"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("équipe")
        verbose_name_plural = _("équipes")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def merge_into(self, target_team, keep_source_leader=False):
        """
        Merges this team (source) into target_team:
        - Creates a slug redirect for the old slug.
        - Moves news and offers to target_team.
        - Adds target_team to all publications associated with source team.
        - Reassigns memberships (without duplicating user memberships).
        - Keeps target_team's leader unless keep_source_leader is explicitly True.
        - Deletes this team.
        """
        from django.db import transaction
        with transaction.atomic():
            # 1. Slug redirect
            TeamSlugRedirect.objects.update_or_create(
                old_slug=self.slug,
                defaults={"team": target_team}
            )

            # 2. News and offers
            self.news.all().update(team=target_team)
            self.offers.all().update(team=target_team)

            # 3. Publications (M2M)
            for pub in self.publications.all():
                pub.teams.add(target_team)
                pub.teams.remove(self)

            # 4. Memberships
            existing_target_users = set(
                target_team.memberships.values_list("user_id", flat=True)
            )
            for membership in self.memberships.all():
                if membership.user_id not in existing_target_users:
                    membership.team = target_team
                    membership.save(update_fields=["team"])
                else:
                    membership.delete()

            # 5. Leader
            if keep_source_leader and self.leader:
                target_team.leader = self.leader
                target_team.save(update_fields=["leader"])

            # 6. Delete source team
            self.delete()


class TeamMembership(models.Model):
    """Links a user to a team with an optional role label."""

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="team_memberships"
    )
    role_in_team = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Rôle dans l'équipe"),
        help_text=_("Ex : Chercheur, Doctorant, Responsable d'équipe"),
    )
    joined_at = models.DateField(auto_now_add=True, verbose_name=_("Membre depuis"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("appartenance à une équipe")
        verbose_name_plural = _("appartenances aux équipes")
        unique_together = ("team", "user")
        ordering = ["team", "user__last_name"]

    def __str__(self):
        return f"{self.user} → {self.team}"


class TeamSlugRedirect(models.Model):
    """
    Keeps old team slugs alive after a rename or merge so that external
    links and bookmarks continue to work.
    The frontend reads /api/teams/slug/<old_slug>/ and is redirected to
    the current team's slug.
    """

    old_slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Ancien slug"))
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="slug_redirects",
        verbose_name=_("Équipe actuelle"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("redirection de slug d'équipe")
        verbose_name_plural = _("redirections de slugs d'équipe")

    def __str__(self):
        return f"{self.old_slug} → {self.team.slug}"
