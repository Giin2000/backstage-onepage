from django.db import models


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    imagen_banner = models.ImageField(upload_to='banners/', blank=True)
    slug = models.SlugField(unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Registro(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    generos = models.TextField()
    experiencia = models.TextField(blank=True)
    comentario = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.evento}'
