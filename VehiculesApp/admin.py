from django.contrib import admin

from .models import Vehicules


@admin.register(Vehicules)
class VehiculesAdmin(admin.ModelAdmin):
    list_display = (
        "immatriculation",
        "capacite_kg",
        "type_vehicules",
        "disponible",
        "entreprise",
    )
    list_display_links = ("immatriculation",)
    list_filter = ("type_vehicules", "disponible", "entreprise")
    search_fields = (
        "immatriculation",
        "entreprise__raison_social",
    )
    list_editable = ("capacite_kg", "type_vehicules", "disponible")
    ordering = ("immatriculation",)
    fieldsets = (
        (
            "Information générales",
            {
                "fields": ("immatriculation", "type_vehicules", "disponible"),
            },
        ),
    )
