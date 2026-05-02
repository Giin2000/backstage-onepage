from django import forms
from .models import Registro

GENEROS_CHOICES = [
    ('Rock', 'Rock'),
    ('Jazz', 'Jazz'),
    ('Electronica', 'Electrónica'),
    ('Hip Hop', 'Hip Hop'),
    ('Pop', 'Pop'),
    ('Indie', 'Indie'),
    ('Urbano', 'Urbano'),
    ('Otro', 'Otro'),
]


class RegistroForm(forms.ModelForm):
    generos = forms.MultipleChoiceField(
        choices=GENEROS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Géneros musicales',
    )

    class Meta:
        model = Registro
        exclude = ('evento', 'fecha_registro')
