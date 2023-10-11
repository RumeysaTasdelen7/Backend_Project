from django.db import models

# Create your models here.

TRANSMISSION = (
    ('a', 'Automatic'),
    ('m', 'Manuel'),
    ('t', 'Triptronic'),
)

FUEL = (
    ('e', 'Electricity'),
    ('h', 'Hybrid'),
    ('g', 'Gasoline'),
    ('d', 'Diesel'),
    ('hy', 'Hydrogen'),
    ('l', 'LPG'),
    ('c', 'CNG'),
)


class Car(models.Model):
    model = models.CharField(max_length=100)
    doors = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField()
    transmission = models.CharField(max_length=10, choices=TRANSMISSION)
    airConditioning = models.BooleanField()
    age = models.PositiveIntegerField()
    pricePerHour = models.DecimalField(max_digits=8, decimal_places=2)
    fuelType = models.CharField(max_length=2, choices=FUEL)
    builtIn = models.BooleanField(default=True)
    image = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.model