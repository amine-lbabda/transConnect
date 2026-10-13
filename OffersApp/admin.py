from django.contrib import admin

from .models import Offres


@admin.register(Offres)
class OffresAdmin(admin.ModelAdmin):
    list_display = (
        "prix",
        "delai_jours",
        "statut",
        "date_proposition",
        "entreprise",
        "vehicule",
        "expedition",
    )
    list_display_links = ("expedition",)
    list_filter = ("statut", "date_proposition")
    search_fields = (
        "statut",
        "entreprise__raison_social",
        "vehicule__immatriculation",
        "expedition__reference",
    )
    list_editable = ("prix", "delai_jours", "statut")
    ordering = ("-date_proposition",)
