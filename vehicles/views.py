from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .models import User

def index(request: HttpRequest):
    return render(request, "vehicles/index.html")


def login_view(request: HttpRequest):
    pass


def register_view(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse("TODO")

    # Any other method will render the form
    return render(request, "vehicles/register.html")