from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import *

app_name = "Escuela"

urlpatterns = [
path('login', views.Login.as_view(), name='login'),
path('panel', views.Panel.as_view(), name='panel'),
path('salir', views.Salir.as_view(), name='salir'),
path('Agregar', views.Agregar.as_view(), name='Agregar'),
path('Lista1', views.Listar_agregar.as_view(), name='Lista1'),
path("eliminar/<int:datos_id>/", views.eliminar, name="eliminar"),
path('editar/<int:datos_id>/', login_required(views.editar), name='editar'),
path("gestion/", views.gestion, name="gestion"),
path("mostrar_notas/<int:notas_id>/", views.mostrar_notas, name="mostrar_notas"),
path("editar_notas/<int:notas_id>/", views.editar_notas, name="editar_notas"),
path("obtener_notas/<int:notas_id>/", views.obtener_notas, name="obtener_notas"),
path('agregar_notas/<int:id>/', views.agregar_notas, name='agregar_notas'),
path('informacion/', views.informacion, name='informacion'),
#path('registro/', views.registro, name='registro'),
path('publicacion/<int:id>/', views.publicacion, name='publicacion'),
#path('logout/', views.logout_view, name='logout'),



]