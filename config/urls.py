from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from registro.views import estadisticas_admin

urlpatterns = [
    path('admin/estadisticas/', estadisticas_admin, name='admin_estadisticas'),
    path('admin/', admin.site.urls),
    path('', include('registro.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
