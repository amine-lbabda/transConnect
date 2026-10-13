from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


def validate_email(email: str):
    if not email:
        raise ValidationError("Email est manquant !")
    if not email.endswith("@gmail.com"):
        raise ValidationError(
            "Seuls les emails appartenant au domaine gmail.com sont acceptés"
        )


REGEX_MATRICULE_VALIDATEUR = RegexValidator(
    regex=r"^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$",
    message="Matricule fiscale pas respectée !",
)


# Create your models here.
class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, editable=False, primary_key=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    role = models.CharField(
        max_length=20,
        choices=[
            ("chargeur", "Chargeur"),
            ("transporteur", "Transporteur"),
            ("administrateur", "administrateur"),
        ],
        default="chargeur",
    )
    telephone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ["email", "telephone"]

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_user_id(cls):
        annee = timezone.now().strftime("%Y")[2:]
        prefix = f"{annee}user"
        last_val = (
            cls.objects.filter(user_id__startswith=prefix).order_by("-user_id").first()
        )
        count_year = (int(last_val[6:]) + 1) % 100 if last_val else 00
        if count_year > 99:
            raise ValidationError("Limite des utilisateurs atteint !")
        return f"{prefix}{count_year:02d}"

    def __str__(self):
        return f"user_id:{self.user_id}\nemail:{self.email}\nrole:{self.role}\ntelephone:{self.telephone}\n"


class Entreprise(models.Model):
    raison_social = models.CharField(max_length=100)
    matricule_fiscal = models.CharField(
        max_length=8,
        unique=True,
        validators=[REGEX_MATRICULE_VALIDATEUR],
    )
    type_entreprise = models.CharField(
        max_length=15,
        choices=[
            ("chargeur", "Chargeur"),
            ("transporteur", "Transporteur"),
        ],
    )
    addresse = models.TextField(validators=[MinValueValidator(20)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(
        "Utilisateur", on_delete=models.CASCADE, related_name="Entreprise"
    )

    def __str__(self):
        return f"raision_social:{self.raison_social}\nmatricule_fiscale:{self.matricule_fiscal}\ntype_entreprise:{self.type_entreprise}\naddresse:{self.addresse}\ncreated_at:{self.created_at}\nupdated_at:{self.updated_at}"
