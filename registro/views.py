from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Evento
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
            registro.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'registro/index.html', {'evento': evento, 'form': form})
