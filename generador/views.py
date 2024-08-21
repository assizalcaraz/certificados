from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import CertificadoForm
from .models import Certificado
import hashlib
import qrcode
from io import BytesIO
from django.core.files import File
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from django.template.loader import get_template
from xhtml2pdf import pisa

# Generar claves RSA (esto normalmente se haría una vez y se almacenaría la clave privada de forma segura)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

def generar_certificado(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            certificado = form.save(commit=False)

            # Crear un string con los datos a tokenizar
            datos = f"{certificado.nombre_participante}{certificado.nombre_curso}{certificado.fecha_emision}"
            certificado.token = hashlib.sha256(datos.encode('utf-8')).hexdigest()

            # Generar una firma digital del token
            firma = private_key.sign(
                datos.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            certificado.firma = firma

            # Generar un código QR con el token y la firma
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(certificado.token)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            # Verifica el nombre del archivo que se está guardando
            print(f"Guardando QR en {certificado.id}.png")

            certificado.codigo_qr.save(f'{certificado.id}.png', File(buffer), save=False)

            # Asegúrate de que el campo de la imagen tiene un valor
            print(f"QR guardado en: {certificado.codigo_qr.path}")

            certificado.save()
            return redirect('detalle_certificado', pk=certificado.pk)
    else:
        form = CertificadoForm()
    return render(request, 'generador/generar_certificado.html', {'form': form})

def detalle_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    return render(request, 'generador/certificado_template.html', {'certificado': certificado})

def exportar_certificado_pdf(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)

    template = get_template('generador/certificado_template.html')
    context = {'certificado': certificado}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{certificado.pk}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response