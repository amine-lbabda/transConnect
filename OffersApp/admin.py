import csv
import typing

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Offres


@admin.register(Offres)
class OffresAdmin(admin.ModelAdmin):
    list_display = (
        "expedition",
        "prix",
        "delai_jours",
        "statut_colore",
        "date_proposition",
        "entreprise",
        "vehicule",
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

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields or ("date_proposition", "statut_colore"))
        if obj and obj.statut == "acceptee":
            for field in ("prix", "delai_jours"):
                if field not in base:
                    base.append(field)
        return base

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

    @admin.action(description="Exporter la séléction en csv")
    def exporter_offres_csv(modeladmin, request, queryset: QuerySet[Offres]):
        res = HttpResponse(content_type="text/csv")
        res["Content-Disposition"] = 'attachement;filename="offres.csv"'
        writter = csv.writer(res)
        writter.writerow(["reference_expedition", "transporteur", "prix", "statut"])
        for offre in queryset.select_related("expedition", "entreprise"):
            writter.writerow(
                [
                    offre.expedition.reference,
                    offre.entreprise.raison_social,
                    offre.prix,
                    offre.statut,
                ]
            )
        return res

    actions: typing.ClassVar = ["exporter_offres_csv"]
