from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ("chargeur", "Chargeur"),
            ("transporteur", "Transporteur"),
            ("administrateur", "administrateur"),
        ],
        default="Chargeur",
    )
    telephone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user_id:{self.user_id}\nemail:{self.email}\nrole:{self.role}\ntelephone:{self.telephone}\n"


class Entreprise(models.Model):
    raison_social = models.CharField(max_length=100)
    matricule_fiscal = models.CharField(max_length=8, unique=True)
    type_entreprise = models.CharField(
        max_length=15,
        choices=[
            ("chargeur", "Chargeur"),
            ("transporteur", "Transporteur"),
        ],
    )
    addresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(
        "Utilisateur", on_delete=models.CASCADE, related_name="Entreprise"
    )

    def __str__(self):
        return f"raision_social:{self.raison_social}\nmatricule_fiscale:{self.matricule_fiscal}\ntype_entreprise:{self.type_entreprise}\naddresse:{self.addresse}\ncreated_at:{self.created_at}\nupdated_at:{self.updated_at}"
