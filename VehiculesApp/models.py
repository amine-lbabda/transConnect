from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from EntrepriseApp.models import Entreprise

# Create your models here.


class Vehicules(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True, validators=[])
    capacite_kg = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, "Une capacité nulle ne peut pas être acceptée")
        ]
    )
    type_vehicules = models.CharField(
        max_length=50,
        choices=[
            ("camionnette", "Camionnette"),
            ("fourgon", "Fourgon"),
            ("camion_porteur", "Camion porteur"),
            ("semi_remorque", "Semi-remorque"),
        ],
    )
    disponible = models.BooleanField(default=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

    def __str__(self):
        return f"Immatriculation:{self.immatriculation}\ncapacite_kg:{self.capacite_kg}\ntype_vehicules:{self.capacite_kg}\ndisponible:{self.disponible}"

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != "transporteur":
            raise ValidationError(
                "La véhicule doit être attaché à une entreprise de type transporteur"
            )
