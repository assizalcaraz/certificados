from django import forms
from .models import Certificado

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['nombre_participante', 'nombre_curso']
