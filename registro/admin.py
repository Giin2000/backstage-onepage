from django.contrib import admin
from .models import Evento, Registro


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'activo')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'ciudad', 'evento', 'fecha_registro')
    list_filter = ('evento', 'fecha_registro')
