import csv

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Evento, Registro

# ── Encabezados del sitio ────────────────────────────────────────────────────
admin.site.site_header = 'Backstage Company'
admin.site.site_title  = 'Backstage · Panel de Control'
admin.site.index_title = 'Bienvenido, Angello — Gestión de eventos y registros'

# Ocultar modelos de autenticación que Angello no necesita
try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


# ── Evento ───────────────────────────────────────────────────────────────────
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display        = ('nombre', 'fecha', 'lugar', 'activo', 'url_evento', 'total_registros')
    list_editable       = ('activo',)
    list_filter         = ('activo', 'fecha')
    search_fields       = ('nombre', 'lugar')
    ordering            = ('-fecha',)
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields     = ('info_qr',)

    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'fecha', 'lugar', 'slug', 'activo'),
        }),
        ('Banner', {
            'fields': ('imagen_banner', 'video_banner'),
        }),
        ('Información para el QR', {
            'fields': ('info_qr',),
        }),
    )

    def changeform_view(self, request, *args, **kwargs):
        self._current_request = request
        return super().changeform_view(request, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['imagen_banner'].help_text = 'JPG o PNG · 1920x600px recomendado · Máx 5MB'
        form.base_fields['video_banner'].help_text = 'MP4 · 1920x600px recomendado · Máx 10MB · Sin audio'
        return form

    @admin.display(description='URL del evento')
    def url_evento(self, obj):
        url = f'/{obj.slug}/'
        return format_html('<code style="font-size:0.85em;user-select:all">{}</code>', url)

    @admin.display(description='Registros')
    def total_registros(self, obj):
        return obj.registro_set.count()

    @admin.display(description='URL pública del evento')
    def info_qr(self, obj):
        if not obj or not obj.slug:
            return 'Guarda el evento primero para ver la URL.'
        url = self._current_request.build_absolute_uri(obj.get_absolute_url())
        return format_html(
            '<p style="font-family:monospace;font-size:1em;padding:8px 12px;'
            'background:#f5f5f5;border-radius:4px;border:1px solid #ddd;'
            'display:inline-block;user-select:all">{}</p>'
            '<p style="margin-top:6px;font-size:0.82em;color:#666">'
            'Comparte esta URL o genera un QR apuntando a ella.</p>',
            url,
        )


# ── Acción CSV ───────────────────────────────────────────────────────────────
def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="registros.csv"'
    response.write('﻿')  # BOM para Excel

    writer = csv.writer(response)
    writer.writerow([
        'Nombre', 'Email', 'Teléfono', 'Ciudad',
        'Géneros', 'Experiencia', 'Evento', 'Fecha de registro', 'Comentario',
    ])
    for r in queryset.select_related('evento'):
        writer.writerow([
            r.nombre, r.email, r.telefono, r.ciudad,
            r.generos, r.experiencia, r.evento.nombre,
            r.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            r.comentario,
        ])
    return response

exportar_csv.short_description = 'Exportar registros seleccionados a CSV'


# ── Registro ─────────────────────────────────────────────────────────────────
@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'email', 'telefono', 'ciudad', 'generos_legible', 'evento', 'fecha_registro')
    list_filter     = ('evento', 'ciudad')
    search_fields   = ('nombre', 'email', 'telefono')
    ordering        = ('-fecha_registro',)
    actions         = [exportar_csv]
    list_per_page   = 50
    readonly_fields = ('fecha_registro',)

    fieldsets = (
        ('Datos personales', {
            'fields': ('nombre', 'email', 'telefono', 'ciudad'),
        }),
        ('Preferencias musicales', {
            'fields': ('generos',),
        }),
        ('Experiencia buscada', {
            'fields': ('experiencia',),
        }),
        ('Comentario', {
            'fields': ('comentario',),
        }),
        ('Metadata', {
            'fields': ('evento', 'fecha_registro'),
        }),
    )

    @admin.display(description='Géneros')
    def generos_legible(self, obj):
        return ', '.join(g.strip() for g in obj.generos.split(',') if g.strip())
