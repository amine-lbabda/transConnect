from decimal import Decimal

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone

TYPE_CAPACITY_RANGES = {
    "camionnette": (Decimal(0), Decimal(1500)),
    "fourgon": (Decimal(1501), Decimal(3500)),
    "camion_porteur": (Decimal(3500), Decimal(19000)),
    "semi_remorque": (Decimal(19000), Decimal(26000)),
}


class Offres(models.Model):
    prix = models.DecimalField(
        decimal_places=10,
        max_digits=13,
        validators=[MinValueValidator(0.0, "Le prix doit être différent de zéro !")],
    )
    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Une offre doit avoir un délai !")]
    )
    statut = models.CharField(
        max_length=20,
        choices=[
            ("proposee", "Proposée"),
            ("acceptee", "Acceptée"),
            ("refusee", "Refusée"),
            ("retiree", "Retirée"),
        ],
        default="proposee",
    )
    date_proposition = models.DateField(auto_now_add=True)
    expedition = models.ForeignKey(
        "ExpeditionsApp.Expedition", on_delete=models.CASCADE, related_name="offres"
    )
    entreprise = models.ForeignKey(
        "EntrepriseApp.Entreprise", on_delete=models.CASCADE, related_name="offres"
    )
    vehicule = models.ForeignKey(
        "VehiculesApp.Vehicules", on_delete=models.CASCADE, related_name="offres"
    )

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != "transporteur":
            raise ValidationError("Le type d'entreprise doit être transporteur !")

        if (
            self.entreprise_id
            and self.vehicule_id
            and self.entreprise_id != self.vehicule.entreprise_id
        ):
            raise ValidationError(
                "Le véhicule doit appartenir à la même entreprise "
                "que le transporteur de l'offre."
            )

        if self.entreprise_id and self.entreprise.type_entreprise != "transporteur":
            raise ValidationError(
                "Une offre ne peut être créée que par un transporteur."
            )

        if self.statut == "proposee":
            exists = (
                Offres.objects.filter(
                    entreprise_id=self.entreprise_id,
                    expedition_id=self.expedition_id,
                    statut="proposee",
                )
                .exclude(pk=self.pk)
                .exists()
            )
            if exists:
                raise ValidationError(
                    "Une entreprise ne peut pas avoir deux offres "
                    "proposées pour la même expédition."
                )

        if self.vehicule_id and self.expedition_id:
            if not self.vehicule.disponible:
                raise ValidationError("Ce véhicule n'est pas disponible.")

            plage = TYPE_CAPACITY_RANGES.get(self.vehicule.type_vehicules)
            if plage is None:
                raise ValidationError(
                    "Le type de véhicule ne possède pas de plage de poids définie."
                )

            poids_min, poids_max = plage
            poids_expedition = self.expedition.poids_kg
            if not poids_min <= poids_expedition <= poids_max:
                raise ValidationError(
                    "Le type de véhicule n'est pas compatible avec "
                    "le poids de l'expédition."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        prev_stat = None
        if self.pk:
            prev_stat = (
                Offres.objects.filter(pk=self.pk)
                .values_list("statut", flat=True)
                .first()
            )
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.statut == "acceptee" and prev_stat != "acceptee":
                self._appliquer_cascade_acceptation()

    def _appliquer_cascade_acceptation(self):
        Expedition = apps.get_model("ExpeditionsApp", "Expedition")
        Expedition.objects.filter(pk=self.expedition_id).update(
            statut="attribuee", updated_at=timezone.now()
        )
        Offres.objects.filter(
            expedition_id=self.expedition_id, statut="proposee"
        ).exclude(pk=self.pk).update(statut="refusee", updated_at=timezone.now())

    def __str__(self):
        return f"Prix:{self.prix}\nDélai:{self.delai_jours}\nStatut:{self.statut}\nDate de proposition:{self.date_proposition}"
