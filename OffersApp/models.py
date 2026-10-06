from django.db import models

# Create your models here.


class Offres(models.Model):
    prix = models.DecimalField(decimal_places=10,max_digits=10)
    delai_jours = models.PositiveIntegerField()
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
    def __str__(self):
        return f'Prix:{self.prix}\nDélai:{self.delai_jours}\nStatut:{self.statut}\nDate de proposition:{self.date_proposition}'
