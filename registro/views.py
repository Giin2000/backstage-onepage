import csv
from collections import Counter
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import ArtistRegistro, Evento, Registro
from .forms import ArtistForm, EventoForm, RegistroForm


@require_http_methods(['GET', 'POST'])
def registro_evento(request, slug):
    evento = get_object_or_404(Evento, slug=slug, activo=True)
    form = RegistroForm()

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = RegistroForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.evento = evento
            generos_list = list(form.cleaned_data['generos'])
            genero_otro = form.cleaned_data.get('genero_otro', '').strip()
            if genero_otro:
                if 'Otro' in generos_list:
                    generos_list.remove('Otro')
                generos_list.append(genero_otro)
            registro.generos = ', '.join(generos_list)
            subgeneros = form.cleaned_data.get('subgeneros', '').strip()
            if subgeneros:
                registro.generos += ', ' + subgeneros
            registro.ciudad = form.cleaned_data.get('ciudad', '')
            experiencia_list = [v for v in form.cleaned_data.get('experiencia', []) if v != 'Otro']
            experiencia_otro = form.cleaned_data.get('experiencia_otro', '').strip()
            if experiencia_otro:
                experiencia_list.append(experiencia_otro)
            registro.experiencia = ', '.join(experiencia_list)
            registro.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'registro/index.html', {'evento': evento, 'form': form})


def _with_pct(items, key='total'):
    items = list(items)
    if not items:
        return items
    max_val = max(item[key] for item in items) or 1
    for item in items:
        item['pct'] = int(item[key] / max_val * 100)
    return items


@staff_member_required
def estadisticas_admin(request):
    por_evento_qs = list(
        Evento.objects.annotate(total=Count('registro')).order_by('-total').values('nombre', 'total')
    )
    por_evento = _with_pct(por_evento_qs)

    top_ciudades_qs = list(
        Registro.objects.values('ciudad').annotate(total=Count('id')).order_by('-total')[:5]
    )
    top_ciudades = _with_pct(top_ciudades_qs)

    counter = Counter()
    for gs in Registro.objects.values_list('generos', flat=True):
        for g in gs.split(','):
            g = g.strip()
            if g:
                counter[g] += 1
    top_5 = counter.most_common(5)
    max_g = top_5[0][1] if top_5 else 1
    top_generos = [
        {'genero': g, 'total': c, 'pct': int(c / max_g * 100)}
        for g, c in top_5
    ]

    hoy = timezone.now().date()
    semana_raw = [
        {'dia': hoy - timedelta(days=i), 'total': Registro.objects.filter(fecha_registro__date=hoy - timedelta(days=i)).count()}
        for i in range(6, -1, -1)
    ]
    max_s = max(s['total'] for s in semana_raw) or 1
    semana = [dict(s, pct=int(s['total'] / max_s * 100)) for s in semana_raw]

    return render(request, 'admin/estadisticas.html', {
        'title': 'Estadísticas',
        'por_evento': por_evento,
        'top_ciudades': top_ciudades,
        'top_generos': top_generos,
        'semana': semana,
    })


# ── Panel de Control ────────────────────────────────────────────────────────

@login_required(login_url='/admin/login/')
def panel_index(request):
    return render(request, 'panel/index.html', {
        'total_eventos': Evento.objects.count(),
        'total_registros': Registro.objects.count(),
    })


@login_required(login_url='/admin/login/')
def panel_evento_form(request, evento_id=None):
    evento = get_object_or_404(Evento, pk=evento_id) if evento_id else None

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            evento = form.save()
            return redirect(f'/studio/evento/{evento.pk}/editar/?guardado=1')
    else:
        form = EventoForm(instance=evento)

    evento_url = request.build_absolute_uri(evento.get_absolute_url()) if evento and evento.slug else None

    return render(request, 'panel/evento_form.html', {
        'form': form,
        'evento': evento,
        'guardado': request.GET.get('guardado') == '1',
        'evento_url': evento_url,
    })


@login_required(login_url='/admin/login/')
def panel_registros(request):
    eventos = Evento.objects.all().order_by('-fecha')
    evento_id = request.GET.get('evento')
    evento_sel = None
    registros = Registro.objects.select_related('evento').order_by('-fecha_registro')

    if evento_id:
        evento_sel = get_object_or_404(Evento, pk=evento_id)
        registros = registros.filter(evento=evento_sel)

    return render(request, 'panel/registros.html', {
        'eventos': eventos,
        'evento_sel': evento_sel,
        'registros': registros,
        'total': registros.count(),
        'evento_id': evento_id or '',
    })


@login_required(login_url='/admin/login/')
def panel_eventos_lista(request):
    eventos = Evento.objects.annotate(total_reg=Count('registro')).order_by('-fecha')
    return render(request, 'panel/eventos_lista.html', {'eventos': eventos})


@require_http_methods(['GET', 'POST'])
def disquera_registro(request):
    form = ArtistForm()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return render(request, 'registro/disquera.html', {'form': form})


@login_required(login_url='/admin/login/')
def panel_artistas(request):
    artistas = ArtistRegistro.objects.order_by('-fecha_registro')

    if request.GET.get('exportar') == '1':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="artistas.csv"'
        response.write('﻿')
        writer = csv.writer(response)
        writer.writerow([
            'Nombre', 'Nombre artístico', 'Email',
            'Instagram', 'TikTok', 'Spotify', 'YouTube',
            'Otro contacto', 'Fecha de registro',
        ])
        for a in artistas:
            writer.writerow([
                a.nombre, a.nombre_artistico, a.email,
                a.instagram, a.tiktok, a.spotify, a.youtube,
                a.otro_contacto, a.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            ])
        return response

    return render(request, 'panel/artistas.html', {'artistas': artistas, 'total': artistas.count()})


@login_required(login_url='/admin/login/')
@require_http_methods(['POST'])
def eliminar_artista(request, pk):
    artista = get_object_or_404(ArtistRegistro, pk=pk)
    artista.delete()
    return redirect('/studio/artistas/')


@login_required(login_url='/admin/login/')
def panel_exportar_csv(request):
    evento_id = request.GET.get('evento')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="registros.csv"'
    response.write('﻿')

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Teléfono', 'Ciudad', 'Géneros', 'Experiencia', 'Evento', 'Fecha'])
    qs = Registro.objects.select_related('evento').order_by('-fecha_registro')
    if evento_id:
        qs = qs.filter(evento_id=evento_id)
    for r in qs:
        writer.writerow([
            r.nombre, r.email, r.telefono, r.ciudad,
            r.generos, r.experiencia, r.evento.nombre,
            r.fecha_registro.strftime('%d/%m/%Y %H:%M'),
        ])
    return response
