from django.urls import path
from . import views

urlpatterns = [
    path('disquera/', views.disquera_registro, name='disquera_registro'),
    path('<slug:slug>/', views.registro_evento, name='registro_evento'),
]
