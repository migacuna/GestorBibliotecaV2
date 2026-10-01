from django.db import models
from datetime import datetime
from biblioteca.models.cliente import Cliente
from biblioteca.models.libro import Libro

class Prestalibro(models.Model):
    prestaLibro_id = models.BigAutoField(primary_key=True)
    fechaPrestamo = models.DateField
    fechaEntrega = models.DateField
    estado =models.BooleanField(default=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_libros = models.ForeignKey(Libro, on_delete=models.CASCADE)
        
    def validaPrestamo(self):
        hoy = datetime.date()
        if hoy >  self.fechaEntrega:
            self.estado = False
            self.save()
            
            