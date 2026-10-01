from django.db import models

class Autor(models.Model):
    autor_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)