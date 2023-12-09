from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class VehicleList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicle_lists")
    name = models.CharField(max_length=64, default="default_list")

class Vehicle(models.Model):
    list_key = models.ForeignKey(VehicleList, on_delete=models.CASCADE, related_name="vehicles")
    VEHICLE_CHOICES = [
        ("cars", "CAR"),
        ("motorcycles", "MOTORCYCLE"),
        ("trucks", "TRUCK")
    ]
    vehicle_type = models.CharField(max_length=11, choices=VEHICLE_CHOICES)
    fipe_code = models.CharField(max_length=20)
    year_id = models.CharField(max_length=20)

    def serialize(self):
        return {
            "vehicleType": self.vehicle_type,
            "fipeCode": self.fipe_code,
            "yearId": self.year_id,
        }