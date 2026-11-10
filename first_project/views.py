from django.http import HttpRequest, HttpResponse


def homies(req: HttpRequest):
    return HttpResponse("<h1>Welcome to TransConnect</h1>")


def homiesNames(req: HttpRequest, nom: str):
    return HttpResponse(f"<h1>Waa {nom} aandk 200 ?</h1>")
