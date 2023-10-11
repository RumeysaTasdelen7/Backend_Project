from django.db import models

# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.CharField(max_length=50)
    body = models.TextField(max_length=200)
    email = models.EmailField()