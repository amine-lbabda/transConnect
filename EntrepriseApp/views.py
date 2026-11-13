from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ExpeditionsApp.models import Expedition
from VehiculesApp.models import Vehicules

from .models import *

# Create your views here.


class EntrepriseCreateView(CreateView):
    model = Entreprise
    template_name = "entreprises/form.html"
    fields = "__all__"
    success_url = reverse_lazy("entreprises:liste")


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = "entreprises/list.html"
    fields = "__all__"
    context_object_name = "Entreprise"


class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    template_name = "entreprises/form.html"
    fields = "__all__"
    success_url = reverse_lazy("entreprises:liste")


class EntrepriseDeleteView(DeleteView):
    model = Entreprise
    template_name = "entreprises/confirm_delete.html"
    context_object_name = "entreprise"
    success_url = reverse_lazy("entreprises:liste")
