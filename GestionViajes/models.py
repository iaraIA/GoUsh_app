from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Viaje(models.Model):
    origen = models.CharField(max_length=30)
    destino = models.CharField(max_length=30)
    fecha = models.DateField()
    observaciones = models.CharField(max_length=300)
    conductor = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

class PasajerosViaje(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
