from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request: HttpRequest):
    return HttpResponse("<h1>Vehicles</h1>")
