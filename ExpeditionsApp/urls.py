from django.urls import path

from .views import *

app_name = "expeditions"
urlpatterns = [
    path("", ListViewExpedition.as_view(), name="liste"),
    path("<str:reference>", detail_expedition, name="details_expedition"),
]
