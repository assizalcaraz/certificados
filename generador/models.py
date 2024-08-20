from django.db import models
import uuid

class Certificado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_participante = models.CharField(max_length=100)
    nombre_curso = models.CharField(max_length=200)
    fecha_emision = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=64, blank=True, editable=False)
    firma = models.BinaryField(blank=True, editable=False)
    codigo_qr = models.ImageField(upload_to='codigos_qr/', blank=True)

    def __str__(self):
        return f"{self.nombre_participante} - {self.nombre_curso}"

