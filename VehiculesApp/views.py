from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import *
from .models import *


# Create your views here.
class VehiculeCreateView(CreateView):
    model = Vehicules
    template_name = "vehicules/form.html"
    fields = "__all__"
    success_url = reverse_lazy("vehicules:liste")

class VehiculeListView(ListView):
    model = Vehicules
    template_name = "vehicules/list.html"
    context_object_name = "vehicules"

class VehiculeUpdateView(UpdateView):
    model = Vehicules
    template_name = "vehicules/form.html"
    form_class = VehiculeForm
    success_url = reverse_lazy("vehicules:liste")

class DeleteViewVehicule(DeleteView):
    model = Vehicules
    template_name = "vehicules/confirm_delete.html"
    context_object_name = "vehicule"
    success_url = reverse_lazy("vehicules:liste")
