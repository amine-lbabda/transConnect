from django.db import models

from EntrepriseApp.models import Entreprise

# Create your models here.


class Vehicules(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    capacite_kg = models.PositiveIntegerField()
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
