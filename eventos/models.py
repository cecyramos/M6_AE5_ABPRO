from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    TIPO_CHOICES = [
        ('conferencia', 'Conferencia'),
        ('concierto', 'Concierto'),
        ('seminario', 'Seminario'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    privado = models.BooleanField(default=False)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_organizados')
    asistentes = models.ManyToManyField(User, related_name='eventos_registrados', blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-creado_en']