from collections import Counter

from django import template
from django.db.models import Count

from registro.models import Evento, Registro

register = template.Library()


@register.simple_tag
def get_stats():
    total_registros = Registro.objects.count()
    total_eventos_activos = Evento.objects.filter(activo=True).count()

    ciudad_qs = (
        Registro.objects
        .values('ciudad')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )
    ciudad_top = ciudad_qs['ciudad'] if ciudad_qs else '—'

    counter = Counter()
    for gs in Registro.objects.values_list('generos', flat=True):
        for g in gs.split(','):
            g = g.strip()
            if g:
                counter[g] += 1
    genero_top = counter.most_common(1)[0][0] if counter else '—'

    return {
        'total_registros': total_registros,
        'total_eventos_activos': total_eventos_activos,
        'ciudad_top': ciudad_top,
        'genero_top': genero_top,
    }


@register.filter
def split_generos(value):
    return [g.strip() for g in value.split(',') if g.strip()]


@register.filter
def porcentaje(value, max_value):
    if not max_value:
        return 0
    return int(value / max_value * 100)
