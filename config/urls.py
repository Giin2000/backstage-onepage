from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from registro.views import (
    estadisticas_admin,
    panel_index,
    panel_evento_form,
    panel_eventos_lista,
    panel_registros,
    panel_exportar_csv,
)

urlpatterns = [
    path('', RedirectView.as_view(url='/stage-lab/', permanent=False)),
    path('admin/estadisticas/', estadisticas_admin, name='admin_estadisticas'),
    path('admin/', admin.site.urls),
    # Panel personalizado
    path('panel/', panel_index, name='panel_index'),
    path('panel/evento/nuevo/', panel_evento_form, name='panel_evento_nuevo'),
    path('panel/evento/<int:evento_id>/editar/', panel_evento_form, name='panel_evento_editar'),
    path('panel/eventos/', panel_eventos_lista, name='panel_eventos_lista'),
    path('panel/registros/', panel_registros, name='panel_registros'),
    path('panel/exportar-csv/', panel_exportar_csv, name='panel_exportar_csv'),
    path('', include('registro.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
