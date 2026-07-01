from django import forms
from .models import ArtistRegistro, Evento, Registro

GENEROS_CHOICES = [
    ('Rock', 'Rock'),
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
    ('Presentarme como artista', 'Presentarme como artista'),
    ('Otro', 'Otro'),
]

CIUDAD_CHOICES = [
    ('', '— Selecciona tu ciudad —'),
    ('Ciudades frecuentes', [
        ('Oxapampa', 'Oxapampa'),
    ]),
    ('Otras ciudades', [
        ('Amazonas', 'Amazonas'),
        ('Áncash', 'Áncash'),
        ('Apurímac', 'Apurímac'),
        ('Arequipa', 'Arequipa'),
        ('Ayacucho', 'Ayacucho'),
        ('Cajamarca', 'Cajamarca'),
        ('Cusco', 'Cusco'),
        ('Huancavelica', 'Huancavelica'),
        ('Huancayo', 'Huancayo'),
        ('Ica', 'Ica'),
        ('Junín', 'Junín'),
        ('La Libertad', 'La Libertad'),
        ('Lambayeque', 'Lambayeque'),
        ('Lima', 'Lima'),
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


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('nombre', 'descripcion', 'fecha', 'lugar', 'imagen_banner', 'video_banner', 'slug', 'activo')
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%dT%H:%M')


class RegistroForm(forms.ModelForm):
    ciudad = forms.ChoiceField(
        choices=CIUDAD_CHOICES,
        label='Ciudad',
    )
    ciudad_otra = forms.CharField(
        label='¿Cuál ciudad?',
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={'placeholder': 'Escribe tu ciudad'}),
    )
    generos = forms.MultipleChoiceField(
        choices=GENEROS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Géneros musicales',
    )
    genero_otro = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '¿Qué género escuchas?'}),
    )
    subgeneros = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    experiencia = forms.MultipleChoiceField(
        choices=EXPERIENCIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Experiencia / Interés',
        required=True,
    )
    experiencia_otro = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Especifica tu interés'}),
    )

    class Meta:
        model = Registro
        exclude = ('evento', 'fecha_registro', 'ciudad', 'experiencia')

    def clean(self):
        cleaned = super().clean()
        ciudad = cleaned.get('ciudad', '')
        if not ciudad:
            self.add_error('ciudad', 'Selecciona tu ciudad.')
        elif ciudad == 'otra':
            otra = cleaned.get('ciudad_otra', '').strip()
            if not otra:
                self.add_error('ciudad_otra', 'Escribe tu ciudad.')
            else:
                cleaned['ciudad'] = otra
        return cleaned


class ArtistForm(forms.ModelForm):
    class Meta:
        model  = ArtistRegistro
        fields = ('nombre', 'nombre_artistico', 'email', 'instagram', 'tiktok', 'spotify', 'youtube', 'otro_contacto')
        widgets = {
            'nombre':           forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}),
            'nombre_artistico': forms.TextInput(attrs={'placeholder': 'Nombre con el que te conocen'}),
            'email':            forms.EmailInput(attrs={'placeholder': 'tucorreo@gmail.com'}),
            'instagram':        forms.TextInput(attrs={'placeholder': '@tunombre'}),
            'tiktok':           forms.TextInput(attrs={'placeholder': '@tunombre'}),
            'spotify':          forms.TextInput(attrs={'placeholder': 'spotify.com/artist/tunombre'}),
            'youtube':          forms.TextInput(attrs={'placeholder': '@tucanal'}),
            'otro_contacto':    forms.TextInput(attrs={'placeholder': 'WhatsApp, SoundCloud, Linktree…'}),
        }
