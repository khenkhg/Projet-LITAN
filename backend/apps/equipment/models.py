from django.db import models
from django.utils.translation import gettext_lazy as _


class Equipment(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nom"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Slug URL"))
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Catégorie"),
        help_text=_("Ex : Stations de calcul, Robotique & Drones, Réseaux & IoT"),
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    specifications = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Caractéristiques"),
        help_text=_('Paires clé-valeur. Ex : {"GPU": "RTX 4090", "RAM": "128 Go"}'),
    )
    location = models.CharField(
        max_length=100, blank=True, verbose_name=_("Localisation")
    )
    # Nullable — ready for a future Phase 2 external booking integration
    booking_url = models.URLField(
        null=True,
        blank=True,
        verbose_name=_("URL de réservation"),
        help_text=_("Prévu pour une future intégration Phase 2."),
    )
    is_operational = models.BooleanField(
        default=True, verbose_name=_("Opérationnel")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("équipement")
        verbose_name_plural = _("équipements")
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class EquipmentPhoto(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(
        upload_to="equipment/photos/", verbose_name=_("Photo")
    )
    caption = models.CharField(
        max_length=200, blank=True, verbose_name=_("Légende")
    )
    is_primary = models.BooleanField(
        default=False, verbose_name=_("Photo principale")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

    class Meta:
        verbose_name = _("photo d'équipement")
        verbose_name_plural = _("photos d'équipement")
        ordering = ["order"]

    def __str__(self):
        return f"Photo de {self.equipment.name}"
