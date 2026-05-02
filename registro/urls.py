from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.registro_evento, name='registro_evento'),
]
