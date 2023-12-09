from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
import requests

# Errors
from django.db.utils import IntegrityError

# Models
from .models import User

api_url = "https://parallelum.com.br/fipe/api/v2"

def index(request: HttpRequest):
    return render(request, "vehicles/index.html")


def login_view(request: HttpRequest):
    if request.method != "POST":
        # Any other method will render this
        return render(request, "vehicles/login.html")
    
    username = request.POST.get("username")
    password = request.POST.get("password")

    # This just checks if some field is missing
    if not (username and password):
        return render(request, "vehicles/login.html", {
            "error_message": "Form field missing"
        })
    
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return redirect("index")
    else:
        return render(request, "vehicles/login.html", {
            "error_message": "Failed to login"
        })


def register_view(request: HttpRequest):
    if request.method != "POST":
        # Any other method will render this
        return render(request, "vehicles/register.html")
    
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    password_confirmation = request.POST.get("password-confirmation")

    # This just checks if some field is missing
    if not (username and email and password and password_confirmation):
        return render(request, "vehicles/register.html", {
            "error_message": "Form field missing"
        })

    if password != password_confirmation:
        return render(request, "vehicles/register.html", {
            "error_message": "Passwords didn't match"
        })
    
    try:
        User.objects.create_user(username, email, password)
    except IntegrityError:
        return render(request, "vehicles/register.html", {
            "error_message": "Username already taken"
        })
    
    # TODO: Give user feedback that account has been created
    return redirect("login")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("index")


def vehicle(request: HttpRequest):
    vehicle_type = request.GET.get("vehicle-type")
    brand_id = request.GET.get("brand-id")
    model_id = request.GET.get("model-id")
    year_id = request.GET.get("year-id")
    
    vehicle_request = requests.get(f"{api_url}/{vehicle_type}/brands/{brand_id}/models/{model_id}/years/{year_id}")

    return render(request, "vehicles/vehicle.html", {
        "vehicle": vehicle_request.json()
    })