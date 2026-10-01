from django.db import models
from biblioteca.models.autor import Autor
from biblioteca.models.cliente import Cliente

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    libro_id = models.BigAutoField(primary_key=True)
    id_autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    
    # NUEVO: Guarda qué cliente tiene el libro (queda vacío/null si está disponible)
    cliente_prestado = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros_prestados')
    
    def prestar(self):
        if self.disponible:
            self.disponible = False
            self.save()
            return True
        return False
    
    def devolver(self):
        self.disponible = True
        self.save()
            