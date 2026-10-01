from biblioteca.models.libro import Libro
from biblioteca.models.autor import Autor
from biblioteca.models.cliente import Cliente
from django.db import transaction

# Aqui es donde va la logica del negocio
#aca van todos los metodos correspondiente al CRUD
# Esta clase servicio se conecta con la Base de datos
class BibliotecaService:
    
    @staticmethod
    def agregar_libro(datos_post):
        #instancia el objeto "genero"    
    
        #instancia el objeto Autor
        autor = Autor.objects.create(
            nombre = datos_post.get('nombre'),
            nacionalidad = datos_post.get('nacionalidad')
        )
        autor.save()
        libro = Libro.objects.create(
            titulo = datos_post.get('titulo'),
            id_autor = autor            
        )
        libro.save()
        return libro
    
    @staticmethod
    @transaction.atomic  #asegura que tanto la actualizacion de Libro como Autor se guarden juntas
    def modificar_libro(datos_post, id):
        libro = Libro.objects.get(libro_id=id)
        libro.titulo = datos_post.get('titulo')
        libro.save()
        autor = libro.id_autor
        autor.nombre = datos_post.get('nombre')
        autor.nacionalidad = datos_post.get('nacionalidad')
        autor.save()   
        return libro
    
    @staticmethod
    def eliminar_libro(id):
        libro = Libro.objects.filter(libro_id = id).first()
        if libro:
            libro.delete()
            return True
        return libro
    
    @staticmethod
    def agregar_usuario():
        return
    
    @staticmethod
    @transaction.atomic 
    def prestar_libro(id, cliente):
        libro = Libro.objects.get(libro_id = id)
        if libro.disponible:
            libro.disponible = False
            libro.cliente_prestado = cliente #Guarda al Cliente
            libro.save()
            
        return libro
    
    @staticmethod
    @transaction.atomic
    def devolver_libro(id):
        libro = Libro.objects.get(libro_id=id)
        
        if not libro.disponible:
            libro.disponible = True
            libro.cliente_prestado = None #libeta el libro del usuario
            libro.save()
            
        return libro    
    
    @staticmethod
    def obtner_estadisticas_admin():
        total_libros = Libro.objects.count()
        libros_disponibles = Libro.objects.filter(disponible=True).count()
        libros_prestados = Libro.objects.filter(disponible=False).count()
        total_usuario = Cliente.objects.count()
        usuarios_con_prestamos = Cliente.objects.filter(libros_prestados=False).distinct().count()
        
        return {
            'total_libros': total_libros,
            'libros_disponibles': libros_disponibles,
            'libros_prestados': libros_prestados,
            'total_usuarios': total_usuario,
            'usuarios_con_prestamos': usuarios_con_prestamos,
        }
        
    @staticmethod    
    def obtner_todos_los_usuarios():
        return Cliente.objects.all().order_by('-cliente_id')
    
    @staticmethod
    def obtner_libros_de_usuario(usuario):
            return Libro.objects.filter(cliente_prestado=usuario, disponible=False)