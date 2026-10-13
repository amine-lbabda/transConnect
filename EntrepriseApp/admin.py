from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Entreprise, Utilisateur


# Register your models here.
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ("user_id", "username", "email", "role", "first_name", "last_name")
    list_filter = ("user_id", "created_at")
    search_fields = ("user_id", "email", "role")
    list_editable = ("first_name", "last_name")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


# admin.site.register(Utilisateur, UtilisateurAdmin)


class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("raison_social", "matricule_fiscal", "type_entreprise")
    list_filter = ("created_at",'type_entreprise')
    search_fields = ('raison_social','type_entreprise')


admin.site.register(Entreprise, EntrepriseAdmin)
