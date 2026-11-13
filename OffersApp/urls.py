from django.urls import path

from .views import *

app_name = "offres"
urlpatterns = [
    path("create/", OffreCreateView.as_view(), name="create"),
    path("", OffresListView.as_view(), name="liste"),
    path("update/<int:pk>/", OffresUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", OffresDeleteView.as_view(), name="delete"),
]
