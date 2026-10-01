from django.contrib import admin
from biblioteca.models.libro import Libro
from biblioteca.models.autor import Autor
from biblioteca.models.cliente import Cliente  # Asegúrate de importar Cliente

# Registra tus modelos aquí para que aparezcan en /admin
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Cliente)  # <--- ¡Añade esta línea!
