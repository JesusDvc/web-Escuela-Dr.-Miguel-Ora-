from django.db import models
from django.contrib.auth.models import AbstractUser




								# MODELOS

#--------------------------------USUARIO------------------------------------------------
class Usuario(AbstractUser):
    #id
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    nivel = models.IntegerField(null=True) 

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )   

    @classmethod
    def numeroUsuarios(self,tipo):
        if tipo == 'administrador':
            return int(self.objects.filter(is_superuser = True).count() )
        elif tipo == 'usuario':
            return int(self.objects.filter(is_superuser = False).count() )

class Datos(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.CharField(max_length=2)
    direccion = models.TextField()
    fecha_nac = models.DateField()
    docente = models.CharField(max_length=50)
    grado = models.CharField(max_length=50)
    ci_representante = models.CharField(max_length=10)
    codigo_notas = models.CharField(max_length=10)
    codigo_salon = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"

class Notas(models.Model):
    estudiante = models.ForeignKey(Datos, related_name='notas', on_delete=models.CASCADE)
    matematica = models.CharField(max_length=500)
    lengua = models.CharField(max_length=500)
    ciencias_sociales = models.CharField(max_length=500)
    ciencias_naturales = models.CharField(max_length=500)
    deporte = models.CharField(max_length=500)
    cultura = models.CharField(max_length=500)

    def __str__(self):
        return self.matematica

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos del modelo Estudiante

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Representante(models.Model):
    ci_representante = models.CharField(max_length=10)
    nombre_representante = models.CharField(max_length=50)
    estudiante = models.ForeignKey(Datos, related_name='representantes', on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre_representante} (ID: {self.id})"

class Docente(models.Model):
    id_docente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10)
    codigo_salon = models.CharField(max_length=10)
    codigo_materia = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id_docente})"

def get_default_codigo_materia():
    return timezone.now().strftime('%Y-%m-%d %H:%M:%S')

class Salon(models.Model):
    codigo_salon = models.CharField(max_length=10)
    estudiante = models.ForeignKey(Datos, related_name='salones', on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    codigo_materia = models.CharField(max_length=10, default=get_default_codigo_materia)

    def __str__(self):
        return f"Código de salón: {self.codigo_salon} - Materia: {self.codigo_materia}"