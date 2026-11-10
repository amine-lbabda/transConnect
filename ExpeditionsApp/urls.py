from django.urls import path

from .views import *

app_name = "expeditions"
urlpatterns = [
    path("", ListViewExpedition.as_view(), name="liste"),
    path("<str:reference>", ExpeditionDetailView.as_view(), name="details_expedition"),
]
