import typing

from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone

from .models import Expedition

admin.site.site_header = "TransConnect - Administration"
admin.site.site_title = "TransConnect"
admin.site.index_title = "Tableau de board"


# Register your models here.
# admin.site.register(Expedition)
class EnRetardFilter(admin.SimpleListFilter):
    title = "en retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [("oui", "Oui"), ("non", "Non")]

    def queryset(self, request, queryset):
        if self.value() == "oui":
            return queryset.filter(
                statut="publiee", date_souhaitte__lt=timezone.now().date()
            )
        if self.value() == "non":
            return queryset.exclude(
                statut="publiee", date_souhaitte__lt=timezone.now().date()
            )
        return queryset


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "ville_depart",
        "ville_arrive",
        "date_souhaitte",
        "poids_kg",
        "statut",
    )
    list_filter = ("created_at", EnRetardFilter)
    search_fields = ("reference", "ville_depart", "ville_arrive")
    list_editable = ("ville_depart", "ville_arrive", "poids_kg")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Informations sur l'expédition",
            {
                "fields": (
                    "ville_depart",
                    "ville_arrive",
                    "description",
                    "date_souhaitte",
                ),
            },
        ),
        (
            "Informations supplémentaires",
            {
                "fields": ("poids_kg", "statut"),
            },
        ),
        ("Date systéme", {"fields": ("created_at", "updated_at")}),
        ("Entreprise", {"fields": ("entreprise",)}),
    )
    readonly_fields = ("created_at", "updated_at")

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def make_livred(self, req: HttpRequest, queryset: QuerySet[Expedition]):
        liste = queryset.filter(statut="en_cours")
        liste_ignored_nbr = queryset.exclude(statut="en_cours").count()
        errors = []
        compteur = 0
        for exp in liste:
            exp.statut = "livrée"
        try:
            exp.save()
            compteur += 1
        except ValidationError as err:
            errors.append(
                f"{exp.reference}: Erreur de modification Statut avec error:{err.messages}"
            )
        if compteur:
            self.message_user(
                req, "Les expéditions ont été cloturé !", messages.SUCCESS
            )
        if liste_ignored_nbr:
            self.message_user(req, "Expéditions ignorés !", messages.WARNING)
        for e in errors:
            self.message_user(req, e, messages.ERROR)

    action: typing.ClassVar = ["make_livred"]
