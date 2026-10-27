from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

# Create your views here.
from .models import Expedition

"""
def liste_expeditions(request):
    expeditions = Expedition.objects.select_related("entreprise").order_by(
        "-created_at"
    )
    return render(request, "expeditions/liste.html", {"expeditions": expeditions})
"""


class ListViewExpedition(ListView):
    model = Expedition
    template_name = "expeditions/liste.html"
    context_object_name = "expeditions"

    def get_queryset(self):
        return (
            Expedition.objects.filter(statut="publiée")
            .select_related("entreprise")
            .order_by("-created_at")
        )


def detail_expedition(request, reference):
    expedition = get_object_or_404(Expedition, reference=reference)
    offres = expedition.offres.select_related("entreprise", "vehicule").order_by(
        "-date_proposition"
    )
    return render(
        request,
        "expeditions/detail.html",
        {"expedition": expedition, "offres": offres},
    )
