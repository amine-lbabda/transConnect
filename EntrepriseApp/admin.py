from django.contrib import admin

from VehiculesApp.models import Vehicules

from .models import Entreprise, Utilisateur


# Register your models here
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "email", "role", "first_name", "last_name")
    list_filter = ("user_id", "created_at")
    search_fields = ("user_id", "email", "role")
    list_editable = ("first_name", "last_name")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Identité de l'utilisateur",
            {
                "fields": (
                    "username",
                    "role",
                    "first_name",
                    "last_name",
                ),
            },
        ),
        ("Contact", {"fields": ("email", "telephone")}),
        ("Date systéme", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


# admin.site.register(Utilisateur, UtilisateurAdmin)


class VehiculeInline(admin.TabularInline):
    model = Vehicules
    fields = ("immatriculation", "capacite_kg", "type_vehicules", "disponible")
    extra = 1

class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]  # noqa: RUF012
    list_display = ("raison_social", "matricule_fiscal", "type_entreprise")
    list_filter = ("created_at", "type_entreprise")
    search_fields = ("raison_social", "type_entreprise")
    fieldsets = (
        (
            "Identité de l'entreprise",
            {
                "fields": ("raison_social", "matricule_fiscal", "type_entreprise"),
            },
        ),
        ("Contact", {"fields": ("addresse", "gerant")}),
        ("Date systéme", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Entreprise, EntrepriseAdmin)
