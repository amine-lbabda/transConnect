from django.contrib import admin
from django.utils.html import format_html

from .models import Offres


@admin.register(Offres)
class OffresAdmin(admin.ModelAdmin):
    list_display = (
        "prix",
        "delai_jours",
        "statut_colore",
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
    list_editable = ("prix", "delai_jours") 
    ordering = ("-date_proposition",)
    autocomplete_fields = ("expedition", "entreprise", "vehicule")
    fieldsets = (
        ("Détails de l'offre", {"fields": ("expedition", "entreprise", "vehicule")}),
        ("Conditions", {"fields": ("prix", "delai_jours")}),
        (
            "Suivi",
            {
                "fields": (
                    "statut_colore",
                    "date_proposition",
                )
            },
        ),
    )
    readonly_fields = ("date_proposition", "statut_colore")

    @admin.display(description="Statut")
    def statut_colore(self, obj):
        couleurs = {
            "proposee": "#F0AD4E",
            "acceptee": "#5CB85C",
            "refusee": "#D9534F",
            "retiree": "#777777",
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, "#999"),
            obj.get_statut_display(),
        )
