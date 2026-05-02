from django import forms
from .models import Registro

GENEROS_CHOICES = [
    ('Techno', 'Techno'),
    ('House', 'House'),
    ('EDM', 'EDM'),
    ('Reggaetón', 'Reggaetón'),
    ('Hip Hop', 'Hip Hop'),
    ('Latin', 'Latin'),
    ('Otro', 'Otro'),
]

EXPERIENCIA_CHOICES = [
    ('Solo asistir a eventos', 'Solo asistir a eventos'),
    ('Conocer artistas', 'Conocer artistas'),
    ('Hacer networking', 'Hacer networking'),
    ('Trabajar en eventos', 'Trabajar en eventos'),
    ('Colaborar con la productora', 'Colaborar con la productora'),
]

CIUDAD_CHOICES = [
    ('', '— Selecciona tu ciudad —'),
    ('Ciudades frecuentes', [
        ('Huancayo', 'Huancayo'),
        ('Lima', 'Lima'),
        ('Oxapampa', 'Oxapampa'),
    ]),
    ('Otros departamentos', [
        ('Amazonas', 'Amazonas'),
        ('Áncash', 'Áncash'),
        ('Apurímac', 'Apurímac'),
        ('Arequipa', 'Arequipa'),
        ('Ayacucho', 'Ayacucho'),
        ('Cajamarca', 'Cajamarca'),
        ('Cusco', 'Cusco'),
        ('Huancavelica', 'Huancavelica'),
        ('Ica', 'Ica'),
        ('Junín', 'Junín'),
        ('La Libertad', 'La Libertad'),
        ('Lambayeque', 'Lambayeque'),
        ('Loreto', 'Loreto'),
        ('Madre de Dios', 'Madre de Dios'),
        ('Moquegua', 'Moquegua'),
        ('Pasco', 'Pasco'),
        ('Piura', 'Piura'),
        ('Puno', 'Puno'),
        ('San Martín', 'San Martín'),
        ('Tacna', 'Tacna'),
        ('Tumbes', 'Tumbes'),
        ('Ucayali', 'Ucayali'),
    ]),
    ('otra', '+ Otra ciudad'),
]


class RegistroForm(forms.ModelForm):
    ciudad = forms.ChoiceField(
        choices=CIUDAD_CHOICES,
        label='Ciudad',
    )
    ciudad_otra = forms.CharField(
        label='¿Cuál ciudad?',
        required=False,
        max_length=80,
    )
    generos = forms.MultipleChoiceField(
        choices=GENEROS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Géneros musicales',
    )
    subgeneros = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    experiencia = forms.MultipleChoiceField(
        choices=EXPERIENCIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Experiencia / Interés',
        required=False,
    )

    class Meta:
        model = Registro
        exclude = ('evento', 'fecha_registro', 'ciudad', 'experiencia')

    def clean(self):
        cleaned = super().clean()
        ciudad = cleaned.get('ciudad', '')
        if ciudad == 'otra':
            otra = cleaned.get('ciudad_otra', '').strip()
            if not otra:
                self.add_error('ciudad_otra', 'Escribe tu ciudad.')
            else:
                cleaned['ciudad'] = otra
        return cleaned
