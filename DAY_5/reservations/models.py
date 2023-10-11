from django.db import models
from cars.models import Car
from users.models import User
from django.utils import timezone

# Create your models here.


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickUpTime = models.DateTimeField(default=timezone.now)
    dropOffTime = models.DateTimeField(default=timezone.now)
    pickUpLocation = models.CharField(max_length=150)
    dropOffLocation = models.CharField(max_length=150)
    status = models.CharField(max_length=20, default='CREATED')
    totalPrice = models.DecimalField(max_digits=20, decimal_places=2)

