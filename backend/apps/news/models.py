from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(max_length=300, verbose_name=_("Titre"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug URL"))
    summary = models.TextField(
        blank=True,
        verbose_name=_("Résumé"),
        help_text=_("Affiché sur la page d'accueil et dans les listes."),
    )
    content = models.TextField(verbose_name=_("Contenu"))
    image = models.ImageField(
        upload_to="news/images/",
        null=True,
        blank=True,
        verbose_name=_("Image à la une"),
    )
    author = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="authored_news",
        verbose_name=_("Auteur"),
    )
    # null = lab-wide / direction news; set = team-specific news
    team = models.ForeignKey(
        "teams.Team",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="news",
        verbose_name=_("Équipe"),
    )
    published_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("Date de publication")
    )
    is_published = models.BooleanField(default=True, verbose_name=_("Publié"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("actualité")
        verbose_name_plural = _("actualités")
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
