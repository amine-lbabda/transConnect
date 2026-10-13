from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# Create your models here.
class Expedition(models.Model):
    reference = models.CharField(max_length=20, unique=True, editable=False)
    ville_depart = models.CharField(max_length=67)
    ville_arrive = models.CharField(max_length=67)
    poids_kg = models.DecimalField(decimal_places=2, max_digits=10)
    date_souhaitte = models.DateField()
    description = models.TextField()
    statut = models.CharField(
        max_length=20,
        choices=[
            ("publiée", "Publiée"),
            ("attribuée", "Attribuée"),
            ("en_cours", "En cours"),
            ("livrée", "Livrée"),
            ("annulée", "Annulée"),
        ],
        default="publiée",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(
        "EntrepriseApp.Entreprise", on_delete=models.CASCADE, related_name="expedition"
    )

    def __str__(self):
        return f"reference:{self.reference}\nville_depart:{self.ville_depart}\nville_arrive:{self.ville_arrive}\npoids_kg:{self.poids_kg}\ndate_souhaittée:{self.date_souhaitte}\ndescription:{self.description}\nstatut:{self.statut}\ncreated_at:{self.created_at}\nupdated_at:{self.updated_at}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        if self.statut != "publiée":
            raise ValidationError("On ne peut pas accepter les offres !")
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime("%Y")
        prefix = f"EXP-{annee}-"
        last_value = (
            cls.objects.filter(reference__startswith=prefix)
            .order_by("-reference")
            .first()
        )
        val = int(last_value.reference[-5:]) + 1 if last_value else 1
        if val > 99999:
            raise ValidationError("La limite des expéditions atteinte !")
        return f"{prefix}{val:05d}"
