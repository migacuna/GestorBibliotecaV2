from django.urls import path
from biblioteca.controlador import views

urlpatterns = [
    path('', views.pagina_principal, name="pagina_principal"),
    path('agregar_libro', views.agregar_libro, name="agregar_libro"),
    path('eliminar_libro/<str:id>/', views.eliminar_libro, name='eliminar_libro'),
    path('modificar_libro/<str:id>/', views.modificar_libro, name="modificar_libro"),
    path('libros/', views.libros, name='libros'),
    path('prestar_libro/<str:id>/', views.prestar_libro, name='prestar_libro'),
    path('devolver_libro/<str:id>', views.devolver_libro, name='devolver_libro'),
    path('dashboard', views.dashboard_view, name="dashboard"),
]
