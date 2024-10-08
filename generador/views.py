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
from django.conf import settings
import os
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

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

            certificado.codigo_qr.save(f'{certificado.id}.png', File(buffer), save=False)
            certificado.save()
            return redirect('detalle_certificado', pk=certificado.pk)
    else:
        form = CertificadoForm()
    return render(request, 'generador/generar_certificado.html', {'form': form})

def detalle_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    qr_code_url = request.build_absolute_uri(certificado.codigo_qr.url)
    return render(request, 'generador/certificado_template.html', {'certificado': certificado, 'qr_code_url': qr_code_url})

def exportar_certificado_pdf(request, pk):
    # Obtener el certificado por su pk
    certificado = get_object_or_404(Certificado, pk=pk)

    # Obtener la URL completa del código QR
    qr_code_url = request.build_absolute_uri(certificado.codigo_qr.url)
    qr_code_path = os.path.join(settings.MEDIA_ROOT, certificado.codigo_qr.name)

    # Agregar mensajes de depuración
    print(f"Generando PDF para certificado ID: {certificado.pk}")
    print(f"URL del QR: {qr_code_url}")
    print(f"Ruta del archivo QR: {qr_code_path}")

    # Verificar si el archivo QR existe
    if not os.path.exists(qr_code_path):
        print(f"ERROR: La ruta del archivo QR no existe: {qr_code_path}")

    # Renderizar la plantilla HTML con el certificado
    # Se añade `for_pdf=True` al contexto para ocultar el enlace de descarga
    html_string = render_to_string('generador/certificado_template.html', {
        'certificado': certificado,
        'for_pdf': True,
        'qr_code_url': qr_code_url,
    })

    # Crear un objeto HTML para WeasyPrint
    html = HTML(string=html_string)

    # Definir la ruta del PDF a guardar
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'certificados_pdf', f'{certificado.pk}.pdf')
    print(f"Ruta del archivo PDF a generar: {pdf_path}")

    # Opcional: Cargar un archivo CSS específico si es necesario
    css_path = os.path.join(settings.STATIC_ROOT, 'css', 'certificado.css')
    print(f"Ruta del archivo CSS: {css_path}")

    # Verificar si el archivo CSS existe
    if not os.path.exists(css_path):
        print(f"ERROR: La ruta del archivo CSS no existe: {css_path}")

    css = CSS(filename=css_path)

    # Configurar la página en orientación horizontal utilizando un CSS inline
    landscape_css = CSS(string='@page { size: A4 landscape; }')

    # Escribir el archivo PDF con orientación horizontal
    try:
        html.write_pdf(pdf_path, stylesheets=[css, landscape_css])
        print("PDF generado exitosamente.")
    except Exception as e:
        print(f"ERROR al generar el PDF: {e}")

    # Devolver el PDF como respuesta HTTP
    try:
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="certificado_{certificado.pk}.pdf"'
            return response
    except Exception as e:
        print(f"ERROR al enviar el PDF como respuesta: {e}")
        return HttpResponse("Error al generar el PDF", status=500)
