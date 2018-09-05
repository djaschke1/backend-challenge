from django.db import models

# Create your models here.

class Pulse(models.Model):
    name = models.CharField(max_length=50)

    # primitive, gaussian, corpse, cinsk, cinbb (implement check!)
    ptype = models.CharField(max_length=9)

    max_rabi_rate = models.FloatField()
    polar_angle = models.FloatField()

    # We need possibility to upload file
    #upload = models.FileField(upload_to='uploads/')
    
