from django.urls import path

from .views import *

app_name = "vehicules"
urlpatterns = [
    path("create/", VehiculeCreateView.as_view(), name="create"),
    path("", VehiculeListView.as_view(), name="liste"),
    path("update/<int:pk>/", VehiculeUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", DeleteViewVehicule.as_view(), name="delete"),
]
