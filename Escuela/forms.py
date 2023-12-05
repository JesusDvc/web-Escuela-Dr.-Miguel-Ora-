from django import forms
from django.contrib.auth.models import User
from .models import *









#--------------------------------    USUARIO   ------------------------------------------------

class LoginFormulario(forms.Form):
    username = forms.CharField(label="Tu nombre de usuario",widget=forms.TextInput(attrs={'placeholder': 'Usuario',
        'class': 'form-control underlined', 'type':'text','id':'user'}))

    password = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
        'class': 'form-control underlined', 'type':'password','id':'password'}))

#_____________________________________ FIN _______________________________________________



class DatosForm(forms.ModelForm):
    class Meta:
        model = Datos
        fields = '__all__'

class NotasForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = '__all__'

class EstudianteForm(forms.ModelForm):
	class Meta:
		model = Estudiante
		fields = '__all__'

