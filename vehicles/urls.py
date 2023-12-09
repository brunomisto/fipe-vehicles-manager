from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("vehicle", views.vehicle, name="vehicle"),
    path("lists", views.vehicle_lists, name="vehicle_lists"),
    path("lists/<str:name>", views.vehicle_list, name="vehicle_list"),
    path("lists/<str:name>/add", views.add_vehicle_list, name="add_vehicle_list")
    # path("add", )
]