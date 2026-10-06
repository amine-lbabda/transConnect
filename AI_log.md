## Entrée [03/10/2026]
- Outil IA utilisé: None
- Prompt: None
- Sortie obtenu (résumé): None
- écrats identifiés vs cahier de charges: 
    1. Type de prix mentionée: CharField mais en réalité c'est DecimalField
    2. Type de delai_jours IntegerField mais en réalité c'est PositiveIntegerField
    3. La méthode `save` n'est pas obligatoire pour le surcharge
    4. date_proposition paramétre dans DateField est auto_now mais en réalité c'est auto_now_add
- Correction apportée et justification:

    ``` 
    class Offres(models.Model):
    prix = models.DecimalFiel(decimal_places=10,max_digits=10)
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
    ```