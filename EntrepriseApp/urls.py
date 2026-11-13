from django.urls import path

from .views import *

app_name = "entreprises"
urlpatterns = [
    path("create/", EntrepriseCreateView.as_view(), name="create"),
    path("", EntrepriseListView.as_view(), name="liste"),
    path("update/<int:pk>/", EntrepriseUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", EntrepriseDeleteView.as_view(), name="delete"),
]
