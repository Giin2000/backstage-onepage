from collections import Counter
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import Evento, Registro
from .forms import RegistroForm


@require_http_methods(['GET', 'POST'])
def registro_evento(request, slug):
    evento = get_object_or_404(Evento, slug=slug, activo=True)
    form = RegistroForm()

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = RegistroForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.evento = evento
            registro.generos = ', '.join(form.cleaned_data['generos'])
            subgeneros = form.cleaned_data.get('subgeneros', '').strip()
            if subgeneros:
                registro.generos += ', ' + subgeneros
            registro.ciudad = form.cleaned_data.get('ciudad', '')
            registro.experiencia = ', '.join(form.cleaned_data.get('experiencia', []))
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
