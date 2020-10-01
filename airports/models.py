from django.db import models

# Create your models here.


class Airport(models.Model):
    id = models.AutoField(primary_key=True)
    iata = models.CharField(max_length=3, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=2, null=False)
    lat = models.DecimalField(max_digits=22, decimal_places=16)
    lon = models.DecimalField(max_digits=22, decimal_places=16)

    def __str__(self):
        return self.iata
