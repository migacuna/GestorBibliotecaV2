from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from biblioteca.models.libro import Libro
from biblioteca.models.cliente import Cliente
from biblioteca.models.prestaLibro import Prestalibro
from biblioteca.servicios.services import BibliotecaService
from django.contrib.auth.decorators import login_required, user_passes_test

#Funcion auxiliar para verificar si es Admin(is_staff o is_superuser)
def es_admin(user):
    return user.is_authenticated and user.is_superuser

def es_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required(login_url='login')
def pagina_principal(request):
    libros = Libro.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pagina_principal.html', {'libros': libros, 'clientes': clientes})

@login_required(login_url='login')
@user_passes_test(es_admin, login_url='pagina_principal')
def agregar_libro(request):
    if request.method == "POST":
        BibliotecaService.agregar_libro(request.POST)
        return redirect('pagina_principal')
    return render(request, 'agregar_libro.html')

@login_required(login_url='login')
@user_passes_test(es_admin, login_url='pagina_principal')
def eliminar_libro(request, id):
    if BibliotecaService.eliminar_libro(id):
        return redirect('pagina_principal')
    return HttpResponse('No se puede eliminar el libro')

@login_required(login_url='login')
@user_passes_test(es_admin, login_url='pagina_principal')
def modificar_libro(request, id):
    # Obtenemos el libro o devolvemos
    libro = get_object_or_404(Libro, libro_id=id)
    if request.method == "POST":
        BibliotecaService.modificar_libro(request.POST, id)
        return redirect('pagina_principal')
    
    context = {
        'libro': libro
    }
    return render(request, 'modificar_libro.html', context)

def libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros.html', {'libros':libros})

@login_required(login_url='login')
def prestar_libro(request, id):
    if request.method == "POST":
        # Si el cliente no existe en la tabla Cliente, lo crea al vuelo usando el username
        cliente_actual, creado = Cliente.objects.get_or_create(
            nombre=request.user.username,
            defaults={'telefono': '000000000', 'estado': True}
        )
        
        # Ejecutamos el préstamo asociándolo a este cliente
        BibliotecaService.prestar_libro(id, cliente_actual)
            
    return redirect('pagina_principal')
    
@login_required(login_url='login')
def devolver_libro(request, id):
    if request.method == "POST":
        BibliotecaService.devolver_libro(id)
    return redirect('pagina_principal')

@login_required(login_url='login')
def dashboard_view(request):
    #validacion del rol de usuario
    if request.user.is_staff or request.user.is_superuser:
        #usuario admin invoca los metodos de la "capa servicio"
        usuarios = BibliotecaService.obtner_todos_los_usuarios()
        estadisticas_libros = BibliotecaService.obtner_estadisticas_admin()
        lista_usuarios = BibliotecaService.obtner_todos_los_usuarios()
        
        #creamos el contexto con la informacion a mostrar el Front del perfil admin
        context_admin = {
            'usuarios': usuarios,
            'total_libros': estadisticas_libros['total_libros'],
            'libros_disponibles': estadisticas_libros['libros_disponibles'],
            'libros_prestados': estadisticas_libros['libros_prestados'],
            'total_usuarios': estadisticas_libros['total_usuarios'],
            'usuario_con_prestamos': estadisticas_libros['usuarios_con_prestamos'],
            'lista_usuarios': lista_usuarios,
        }
        #redireccion la informacion solicitada al front
        return render(request, 'dashboard_admin.html', context_admin)
    else:
        #usuario normal
        try:
            #rescatando al usuario actual
            cliente_actual = Cliente.objects.get(nombre=request.user.username)
        except:
            # rescata el usuario "invitado"
            cliente_actual = None
        #creamos el contexto con la informacion del perfil usuario a mostrar en el front si es usuario logueado  
        libros_mios = BibliotecaService.obtner_libros_de_usuario(cliente_actual) if cliente_actual else []
        context_user = {
            'libros_mios': libros_mios,
        }
        return render(request, 'dashboard_usuario.html', context_user)
        