from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

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


# def detail_expedition(request, reference):
#     expedition = get_object_or_404(Expedition, reference=reference)
#     offres = expedition.offres.select_related("entreprise", "vehicule").order_by(
#         "-date_proposition"
#     )
#     return render(
#         request,
#         "expeditions/detail.html",
#         {"expedition": expedition, "offres": offres},
#     )


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = "expeditions/detail.html"
    context_object_name = "expedition"

    slug_field = "reference"
    slug_url_kwarg = "reference"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offres"] = self.object.offres.select_related("entreprise", "vehicule")
        return context
