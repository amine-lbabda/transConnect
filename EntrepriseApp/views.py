from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import *
from .models import *

# Create your views here.


class EntrepriseCreateView(CreateView):
    model = Entreprise
    template_name = "entreprises/form.html"
    fields = ("raison_social", "matricule_fiscal", "type_entreprise", "addresse")
    success_url = reverse_lazy("entreprises:liste")

    def form_valid(self, form):
        form.instance.gerant = self.request.user
        return super().form_valid(form)


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = "entreprises/list.html"
    fields = "__all__"
    context_object_name = "entreprises"


class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    template_name = "entreprises/form.html"
    fields = "__all__"
    success_url = reverse_lazy("entreprises:liste")


class EntrepriseDeleteView(LoginRequiredMixin, DeleteView):
    model = Entreprise
    template_name = "entreprises/confirm_delete.html"
    context_object_name = "entreprise"
    success_url = reverse_lazy("entreprises:liste")


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = Utilisateur
    template_name = "registration/register.html"
    success_url = reverse_lazy("entreprises:create")

    def form_valid(self, form):
        response = super().form_valid(form)  # crée l'utilisateur (self.object)
        login(self.request, self.object)  # ouvre directement sa session
        return response
