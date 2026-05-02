from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from registro.views import estadisticas_admin

urlpatterns = [
    path('', RedirectView.as_view(url='/stage-lab/', permanent=False)),
    path('admin/estadisticas/', estadisticas_admin, name='admin_estadisticas'),
    path('admin/', admin.site.urls),
    path('', include('registro.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
