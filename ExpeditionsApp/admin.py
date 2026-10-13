import django.contrib.auth.admin
from django.contrib import admin

from .models import Expedition


# Register your models here.
# admin.site.register(Expedition)
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
    list_filter = ("created_at",)
    search_fields = ("reference", "ville_depart", "ville_arrive")
    list_editable = ("ville_depart", "ville_arrive", "poids_kg")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    