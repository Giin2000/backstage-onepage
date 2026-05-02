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

ORIGEN_CHOICES = [
    ('', '— Selecciona tu origen —'),
    ('nacional', 'Nacional - Perú'),
    ('internacional', 'Internacional'),
]

DEPARTAMENTOS_CHOICES = [
    ('', '— Selecciona un departamento —'),
    ('Lima', 'Lima'),
    ('Arequipa', 'Arequipa'),
    ('Cusco', 'Cusco'),
    ('Junín', 'Junín'),
    ('La Libertad', 'La Libertad'),
    ('Piura', 'Piura'),
    ('Lambayeque', 'Lambayeque'),
    ('Áncash', 'Áncash'),
    ('Loreto', 'Loreto'),
    ('Puno', 'Puno'),
    ('Cajamarca', 'Cajamarca'),
    ('Ica', 'Ica'),
    ('San Martín', 'San Martín'),
    ('Huánuco', 'Huánuco'),
    ('Ucayali', 'Ucayali'),
    ('Ayacucho', 'Ayacucho'),
    ('Apurímac', 'Apurímac'),
    ('Moquegua', 'Moquegua'),
    ('Tacna', 'Tacna'),
    ('Tumbes', 'Tumbes'),
    ('Pasco', 'Pasco'),
    ('Madre de Dios', 'Madre de Dios'),
    ('Amazonas', 'Amazonas'),
    ('Huancavelica', 'Huancavelica'),
]


class RegistroForm(forms.ModelForm):
    origen = forms.ChoiceField(
        choices=ORIGEN_CHOICES,
        label='Origen',
    )
    ciudad_nacional = forms.ChoiceField(
        choices=DEPARTAMENTOS_CHOICES,
        label='Departamento',
        required=False,
    )
    ciudad_internacional = forms.CharField(
        label='País / Ciudad',
        required=False,
        max_length=80,
    )
    generos = forms.MultipleChoiceField(
        choices=GENEROS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Géneros musicales',
    )

    class Meta:
        model = Registro
        exclude = ('evento', 'fecha_registro', 'ciudad')

    def clean(self):
        cleaned = super().clean()
        origen = cleaned.get('origen')
        if origen == 'nacional':
            dep = cleaned.get('ciudad_nacional', '').strip()
            if not dep:
                self.add_error('ciudad_nacional', 'Selecciona un departamento.')
            else:
                cleaned['ciudad'] = f'Nacional - {dep}'
        elif origen == 'internacional':
            ciudad_int = cleaned.get('ciudad_internacional', '').strip()
            if not ciudad_int:
                self.add_error('ciudad_internacional', 'Escribe tu país/ciudad.')
            else:
                cleaned['ciudad'] = f'Internacional - {ciudad_int}'
        return cleaned
