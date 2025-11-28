from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'organizador', 'privado', 'creado_en')
    list_filter = ('tipo', 'privado', 'creado_en')
    search_fields = ('titulo', 'descripcion')


# Desregistrar el UserAdmin por defecto y registrar el personalizado
admin.site.unregister(User)


@admin.register(User)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_grupos', 'is_staff', 'is_superuser')
    list_filter = ('groups', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email')
    
    def get_grupos(self, obj):
        """Muestra los grupos a los que pertenece el usuario"""
        grupos = obj.groups.all()
        if grupos:
            return ", ".join([g.name for g in grupos])
        return "Sin grupo asignado"
    
    get_grupos.short_description = 'Grupo'