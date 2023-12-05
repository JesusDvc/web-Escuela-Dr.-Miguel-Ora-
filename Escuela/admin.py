from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import LoginFormulario
from .models import *

class UsuarioAdmin(UserAdmin):
    add_form = LoginFormulario
    #form = CustomUserChangeForm
    model = Usuario
    list_display = ['email', 'username',]

# Register your models here.
admin.site.register(Datos)
admin.site.register(Notas)
admin.site.register(Estudiante)
admin.site.register(Usuario, UsuarioAdmin)