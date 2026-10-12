from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Offres(models.Model):
    prix = models.DecimalField(
        decimal_places=10,
        max_digits=10,
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

    def save(self, *args, **kwargs):
        if self.entreprise_id != self.vehicule.entreprise_id:
            raise ValidationError(
                "La véhicule doit appartenir à la même entreprise que le transporteur de l'offre"
            )
        if self.entreprise.type_entreprise != "transporteur":
            raise ValidationError(
                "Une offre ne peut pas être crée que par un transporteur !"
            )
        if self.statut == "proposee":
            exists = (
                Offres.objects.filter(
                    entreprise_id=self.entreprise_id,
                    expedition_id=self.expedition_id,
                    statut="propsee",
                )
                .exclude(pk=self.pk)
                .exists()
            )
            if exists:
                raise ValidationError("On ne peut pas avoir deux offres simultanéments")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prix:{self.prix}\nDélai:{self.delai_jours}\nStatut:{self.statut}\nDate de proposition:{self.date_proposition}"
