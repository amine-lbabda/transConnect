from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from EntrepriseApp.models import Entreprise
from ExpeditionsApp.models import Expedition
from VehiculesApp.models import Vehicules

from .models import *


class OffreCreateView(CreateView):
    model = Offres
    template_name = "offres/form.html"
    fields = ["expedition", "vehicule", "prix", "delai_jours"]  # noqa: RUF012

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["expedition"].queryset = Expedition.objects.filter(statut="publiee")
        form.fields["vehicule"].queryset = Vehicules.objects.filter(
            entreprise=self.get_entreprise_courante(), disponible=True
        )
        return form

    def form_valid(self, form):
        form.instance.transporteur = self.get_entreprise_courante()
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.messages)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse(
            "expeditions:detail", kwargs={"reference": self.object.expedition.reference}
        )

    def get_entreprise_courante(self):
        return get_object_or_404(
            Entreprise, pk=self.kwargs["id"], type_entreprise="transporteur"
        )


class OffresListView(ListView):
    model = Offres
    template_name = "forms/list.html"
    fields = "__all__"
    context_object_name = "Offres"


class OffresUpdateView(UpdateView):
    model = Vehicules
    template_name = "vehicules/form.html"
    fields = ["expedition", "vehicule", "prix", "delai_jours"]  # noqa: RUF012

    def get_success_url(self):
        return reverse(
            "expeditions:detail", kwargs={"reference": self.object.expedition.reference}
        )


class OffresDeleteView(DeleteView):
    model = Offres
    template_name = "forms/confirm_delete.html"
    context_object_name = "Offre"
