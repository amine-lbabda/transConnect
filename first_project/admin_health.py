from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone

from EntrepriseApp.models import Entreprise
from ExpeditionsApp.models import Expedition
from OffersApp.models import Offres


def health_check(request):
    transporteurs_sans_flottes = (
        (Entreprise.objects.filter(type_entreprise="transporteur"))
        .annotate(nb_vehicules=Count("vehicules"))
        .filter(nb_vehicules=0)
    )
    offres_orphelins = Offres.objects.exclude(
        expedition__statut__in=["publiée", "attribuée"]
    )
    expedition_blocked = Expedition.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    )
    vehicules_incoherents = Offres.objects.filter(
        vehicule__disponible=True, statut="acceptée"
    )
    doublons_propositions = (
        Offres.objects.filter(statut="proposée")
        .values("expedition_id", "entreprise_id")
        .annotate(nb_offres=Count("id"))
        .filter(nb_offres__gt=1)
    )
    transpoteur_response = "".join(
        f"<li>{transporteur}</li>"
        for transporteur in transporteurs_sans_flottes
        if len(transporteurs_sans_flottes) > 0
    )
    offres_response = "".join(
        f"<li>{offre}</li>" for offre in offres_orphelins if len(offres_orphelins) > 0
    )
    expedition_response = "".join(
        f"<li>{expedition.reference}</li>"
        for expedition in expedition_blocked
        if len(expedition_blocked) > 0
    )
    vehicules_response = "".join(
        f"<li>{vehicule.id}</li>"
        for vehicule in vehicules_incoherents
        if len(vehicules_incoherents) > 0
    )
    doublons_reponse = "".join(
        f"<li>{doublon}</li>" for doublon in doublons_propositions
    )
    return HttpResponse(f"""
                        <h1>TransConnect health check </h1>
                        <ul>Transporteurs sans flotte:{transpoteur_response if len(transpoteur_response) > 0 else "Tous les transporteurs ont des véhicules"}</ul>
                        <ul>Offres orphelines:{offres_response if len(offres_response) > 0 else "Tous les offres acceptés ont une expédition dont elle n'est plus au statut publiée ou attribuée"}</ul>
                        <ul>Expéditions bloquées:{expedition_response if len(expedition_response) > 0 else "Pas d'expédition bloqué !"}</ul>
                        <ul>Incohérence de disponibilité:{vehicules_response if len(vehicules_response) > 0 else "Pas d'incohérence de disponibilité !"}</ul>
                        <ul>Doublons de proposition:{doublons_reponse if len(doublons_reponse) > 0 else "Pas de doublons"}</ul>
                        """)


_original_get_urls = admin.site.get_urls


def get_urls():
    custom_urls = [
        path("health-check/", admin.site.admin_view(health_check), name="health-check")
    ]
    return custom_urls + _original_get_urls()


admin.site.get_urls = get_urls
