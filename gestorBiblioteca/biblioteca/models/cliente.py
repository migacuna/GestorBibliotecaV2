from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=9)
    estado = models.BooleanField(default=True)
    # BigAutoField es un standard de clave primarias
    cliente_id = models.BigAutoField(primary_key=True)
    
    # Estado indica si el cliente esta habilitado para pedir prestado
    def estadoCliente(self):
        if self.estado:
            self.estado = True
        else:
            self.estado = False
        self.save()
        
    def __str__(self):
        # Usamos return y un texto formateado con el nombre y su estado
        estado_texto = "Activo" if self.estado else "Inactivo"
        return f"{self.nombre} ({estado_texto})"