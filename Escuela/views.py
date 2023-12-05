from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.contrib import messages
from django.core.management import call_command
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from decimal import Decimal
import json
from Escuela.mensajes import *
from .models import *
from .forms import *
from .funciones import *
from django.views import generic

function = Function()




class Login(View):
    
    def post(self,request):
        form = LoginFormulario(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            clave = form.cleaned_data['password']
            logeado = authenticate(request, username=usuario, password=clave)
            if logeado:
                login(request,logeado)
                texto = function.mensaje("Sistema Escuela","Bienvenido al Sistema:                  "
                    +'username',"success")
                messages.add_message(request, messages.SUCCESS,texto)
                return HttpResponseRedirect('/Escuela/panel')
            else:
                return render(request, 'Escuela/login.html', {'form': form})


    def get(self,request):
        if request.user.is_authenticated == True:
            return HttpResponseRedirect('/Escuela/panel')

        form = LoginFormulario()
        return render(request, 'Escuela/login.html', {'form': form})



#Panel de inicio y vista principal------------------------------------------------#
class Panel(LoginRequiredMixin, View):
    #De no estar logeado, el usuario sera redirigido a la pagina de Login
    #Las dos variables son la pagina a redirigir y el campo adicional, respectivamente
    login_url = '/Escuela/login'
    redirect_field_name = None

    def get(self, request):
        from datetime import date
        #Recupera los datos del usuario despues del login
        contexto = {'usuario': request.user.username,
                    'id_usuario':request.user.id,
                   'nombre': request.user.first_name,
                   'apellido': request.user.last_name,
                   'correo': request.user.email,
                   'fecha':  date.today(),
                   'usuariosRegistrados' : Usuario.numeroRegistrados(),
                   'administradores': Usuario.numeroUsuarios('administrador'),
                   'usuarios': Usuario.numeroUsuarios('usuario')

        }


        return render(request, 'Escuela/panel.html',contexto)
#Fin de vista----------------------------------------------------------------------#




#Maneja la salida del usuario------------------------------------------------------#
class Salir(LoginRequiredMixin, View):
    #Sale de la sesion actual
    login_url = 'Escuela/login'
    redirect_field_name = None

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/Escuela/login')
#Fin de vista----------------------------------------------------------------------#






class Agregar(LoginRequiredMixin, View):
    login_url = '/Escuela/login'
    redirect_field_name = None

    def post(self, request):
        form = DatosForm(request.POST)

        if form.is_valid():
            form.save()
            
            form = DatosForm()
            texto = function.mensaje("Estudiante","Estudiante registrado exitosamente.","success")
            messages.add_message(request, messages.SUCCESS,texto)
            request.session['agregarProcesada'] = 'agregado'
            return HttpResponseRedirect("/Escuela/Agregar")
        else:
            return render(request, 'todo/agregar.html', {'form': form})

    def get(self,request):
        form = DatosForm()
        contexto = {'form':form , 'modo':request.session.get('agregarProcesada')}   
        contexto = complementarContexto(contexto,request.user)  
        return render(request, 'todo/agregar.html', contexto)



#Crea una lista de los clientes, 10 por pagina----------------------------------------#
class Listar_agregar(LoginRequiredMixin, View):
    login_url = '/Escuela/login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        #Saca una lista de todos los clientes de la BDD
        clientes = Datos.objects.all()                
        contexto = {'tabla': clientes}
        contexto = complementarContexto(contexto,request.user)         

        return render(request, 'todo/listar_agregar.html',contexto) 
#Fin de vista--------------------------------------------------------------------------#


def eliminar(request, datos_id):
    datos = Datos.objects.filter(id=datos_id)
    
    if datos.exists():
        datos.delete()
        return redirect('todo/listar_agregar.html',contexto)
    else:
        return render(request, 'todo/error.html', {'mensaje': 'El dato no existe'})


def editar(request, datos_id):
    datos = Datos.objects.filter(id=datos_id)
    
    if datos.exists():
        datos = datos.first()
        if request.method == "POST":
            form = DatosForm(request.POST, instance=datos)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DatosForm(instance=datos)

        context = {"form": form}
        return render(request, "todo/editar.html", context)
    else:
        return render(request, 'todo/error.html', {'mensaje': 'El dato no existe'})

def gestion(request):
    datos = Datos.objects.all()
    context = {'datos': datos}
    return render(request, 'todo/gestion.html', context)

def mostrar_notas(request, notas_id):
    try:
        notas = Notas.objects.get(id=notas_id)
        return render(request, 'todo/mostrar_notas.html', {'notas': notas})
    except Notas.DoesNotExist:
        return render(request, 'todo/error.html', {'mensaje': 'Las notas no existen'})

def editar_notas(request, notas_id):
    try:
        nota = Notas.objects.get(id=notas_id)
    except Notas.DoesNotExist:
        return render(request, 'todo/error.html', {'mensaje': 'Las notas no existen'})
    
    if request.method == "POST":
        form = NotasForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('mostrar_notas', notas_id=notas_id)
    else:
        form = NotasForm(instance=nota)
    
    context = {'form': form, 'nota': nota}
    return render(request, 'todo/editar_notas.html', context)

def obtener_notas(request, notas_id):
    try:
        notas = Notas.objects.get(pk=notas_id)
    except Notas.DoesNotExist:
        return JsonResponse({'error': 'Las notas no existen'}, status=404)

    data = {
        'estudiante': notas.estudiante.nombre,
        'matematica': notas.matematica,
        'lengua': notas.lengua,
        'ciencias_sociales': notas.ciencias_sociales,
        'ciencias_naturales': notas.ciencias_naturales,
        'deporte': notas.deporte,
        'cultura': notas.cultura
    }
    return JsonResponse(data)

def agregar_notas(request, id):
    if request.method == 'GET':
        # Código para manejar la solicitud GET aquí
        form = NotasForm()  # Crear el formulario NotasForm
        return render(request, 'todo/agregar_notas.html', {'form': form})  # Renderizar la plantilla con el formulario

    if request.method == 'POST':
        form = NotasForm(request.POST)
        if form.is_valid():
            notas = form.save(commit=False)
            notas.usuario_id = id
            notas.save()
            return redirect('usuario', id=id)
        # No necesitas crear un nuevo formulario aquí
        return render(request, 'todo/agregar_notas.html', {'form': form})  # Renderizar la plantilla con el formulario no válido

def informacion(request):
    usuario_actual = request.user  # Obtener el usuario autenticado actualmente
    # Aquí puedes agregar lógica para obtener la información del usuario_actual
    # Por ejemplo, obtener el nombre, correo, etc.
    contexto = {
        'usuario_actual': usuario_actual,
        # Agregar más información del usuario que desees mostrar en la plantilla
    }
    return render(request, 'todo/informacion.html', contexto)

"""def usuario(request, id):
    user = User.objects.get(id=id)
    # Resto de la lógica de la vista 'usuario'
    return render(request, 'usuario.html', {'user': user})"""

def publicacion(request, id):
    publicacion = Publicacion.objects.get(pk=id)
    return render(request, 'publicacion.html', {'publicacion': publicacion})

"""def agregar_usuario(request):
    # Obtener los datos del formulario
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    # Crear el usuario en la base de datos
    usuario = Usuario.objects.create(nombre=nombre, apellido=apellido)
    # Redireccionar a la página del usuario recién creado
    return HttpResponseRedirect(reverse('usuario', args=[usuario.id]))

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            return redirect('usuario')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def crear_usuario(request):
    # Código para crear un usuario
    user = User.objects.create(username='usuario1')
    user.save()

    return HttpResponse("Usuario creado con éxito")

def exit(request):
    logout(request)
    return redirect('todo/home.html')

def entrance(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('todo/home.html')
    else:
        return redirect('entrance')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Manejar el caso de inicio de sesión fallido
            pass
    return render(request, 'todo/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página home.html después del registro exitoso
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})"""
#Muestra el perfil del usuario logeado actualmente---------------------------------#
