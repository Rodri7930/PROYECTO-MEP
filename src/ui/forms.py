
"""Formularios y validaciones de Magic Experiences Perú."""

import re

from django import forms


class PaqueteForm(forms.Form):
    DESTINOS = [
        ("", "Seleccione un destino"),
        ("cusco", "Cusco"),
        ("machu_picchu", "Machu Picchu"),
        ("valle_sagrado", "Valle Sagrado"),
        ("pisac", "Pisac"),
        ("ollantaytambo", "Ollantaytambo"),
    ]

    nombre = forms.CharField(
        label="Nombre del paquete",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. Cusco Cultural",
                "class": "campo-formulario",
            }
        ),
    )

    destino = forms.ChoiceField(
        label="Destino principal",
        choices=DESTINOS,
        required=True,
        widget=forms.Select(
            attrs={"class": "campo-formulario"}
        ),
    )

    duracion = forms.IntegerField(
        label="Duración (días)",
        min_value=1,
        required=True,
        widget=forms.NumberInput(
            attrs={
                "min": "1",
                "step": "1",
                "class": "campo-formulario",
            }
        ),
    )

    pasajeros = forms.IntegerField(
        label="Pasajeros",
        min_value=1,
        required=True,
        widget=forms.NumberInput(
            attrs={
                "min": "1",
                "step": "1",
                "class": "campo-formulario",
            }
        ),
    )

    costo_objetivo = forms.DecimalField(
        label="Costo objetivo interno (USD)",
        min_value=0,
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "min": "0",
                "step": "0.01",
                "class": "campo-formulario",
                "placeholder": "Opcional",
            }
        ),
    )

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if not re.fullmatch(r"[^\W\d_]+(?:[ '\-][^\W\d_]+)*", nombre, re.UNICODE):
            raise forms.ValidationError(
                "El nombre solo debe contener letras y espacios."
            )

        return nombre


class PersonalizarPaqueteForm(PaqueteForm):
    """Formulario para configurar un paquete personalizado."""

    observaciones = forms.CharField(
        label="Observaciones",
        required=False,
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "campo-formulario",
                "rows": 4,
                "placeholder": (
                    "Describe las preferencias, actividades "
                    "o necesidades del cliente."
                ),
            }
        ),
    )
