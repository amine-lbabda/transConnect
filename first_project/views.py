from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def homies(req: HttpRequest):
    return render(req, "home.html")


def homiesNames(req: HttpRequest, nom: str):
    return HttpResponse(f"<h1>Waa {nom} aandk 200 ?</h1>")
