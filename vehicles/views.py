from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests

# Errors
from django.db.utils import IntegrityError

# Models
from .models import User, VehicleList, Vehicle

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
            "error_message": "Credentials not found"
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
    vehicle_type = request.GET.get("type")
    brand_id = request.GET.get("brand")
    model_id = request.GET.get("model")
    year_id = request.GET.get("year")
    
    vehicle_request = requests.get(f"{api_url}/{vehicle_type}/brands/{brand_id}/models/{model_id}/years/{year_id}")

    return render(request, "vehicles/vehicle.html", {
        "vehicle": vehicle_request.json()
    })


@login_required
def add_vehicle_list(request: HttpRequest, name):
    if request.method != "POST":
        return JsonResponse({"error": "Expected POST method"})
    
    try:
        VehicleList.objects.get(owner=request.user, name=name)
        return JsonResponse({"error": f"Vehicle list '{name}' already exists"})
    except:
        pass
    
    vehicle_list_object = VehicleList(owner=request.user, name=name)
    vehicle_list_object.save()
    return JsonResponse({"message": "Sucessfuly added new VehicleList"})


@login_required
def vehicle_list(request: HttpRequest, name):
    try:
        vehicle_list_object = VehicleList.objects.get(owner=request.user, name=name)
    except:
        return JsonResponse({"error": f"Vehicle list {name} not found"})
    
    return JsonResponse({
        "name": vehicle_list_object.name,
        "vehicles": [vehicle_object.serialize() for vehicle_object in vehicle_list_object.vehicles.iterator()]
    })


@login_required
def vehicle_lists(request: HttpRequest):
    user_vehicle_lists = request.user.vehicle_lists.iterator()

    return JsonResponse({
        "lists": [vehicle_list_object.name for vehicle_list_object in user_vehicle_lists]
    })


@login_required
def add_vehicle(request: HttpRequest, vehicle_list):
    vehicle_type = request.POST.get("vehicle-type")
    fipe_code = request.POST.get("fipe-code")
    year_id = request.POST.get("year-id")