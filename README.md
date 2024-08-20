Aquí tienes un archivo `README.md` actualizado que puedes usar para tu repositorio de GitHub. He incluido tu repositorio y email de contacto:

### `README.md`

```markdown
# Proyecto de Generación de Certificados

Este proyecto es una aplicación web basada en Django que permite generar certificados de participación para cursos y eventos. Los certificados generados incluyen un código QR único para la verificación, y están diseñados con patrones de seguridad avanzados.

## Características

- Generación de certificados de participación personalizados.
- Inclusión de códigos QR con verificación mediante criptografía.
- Diseño elegante y profesional con patrones de seguridad en el fondo.
- Exportación de certificados a formato PDF.
- Interfaz simple y fácil de usar.

## Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu entorno:

- Python 3.8 o superior
- Django 4.2 o superior
- Librerías adicionales: `qrcode`, `Pillow`, `cryptography`

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/assizalcaraz/certificados.git
   cd certificados
   ```

2. **Crea un entorno virtual:**

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Realiza las migraciones de la base de datos:**

   ```bash
   python manage.py migrate
   ```

5. **Ejecuta el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

   La aplicación estará disponible en `http://localhost:8000/`.

## Uso

1. **Acceso a la interfaz de generación de certificados:**
   - Visita `http://localhost:8000/certificados/generar/` para acceder a la interfaz donde puedes introducir los datos del participante y generar el certificado.

2. **Verificación del certificado:**
   - El código QR generado en cada certificado puede ser escaneado para verificar la autenticidad del mismo.

3. **Administrador de Django:**
   - Puedes acceder a la interfaz de administración de Django en `http://localhost:8000/admin/` para gestionar los registros de certificados y usuarios.
   - Asegúrate de crear un superusuario para acceder:
     ```bash
     python manage.py createsuperuser
     ```

## Estructura del Proyecto

```plaintext
certificados/
├── certificados/         # Configuración principal del proyecto Django
├── codigos_qr/           # Códigos QR generados
├── db.sqlite3            # Base de datos SQLite (ignorados en el .gitignore)
├── generador/            # Aplicación Django para la generación de certificados
│   ├── migrations/       # Migraciones de la base de datos
│   ├── templates/        # Plantillas HTML para las vistas
│   ├── admin.py          # Configuración del panel de administración
│   ├── forms.py          # Formularios de la aplicación
│   ├── models.py         # Modelos de la aplicación
│   ├── urls.py           # URLs específicas de la aplicación
│   └── views.py          # Vistas de la aplicación
├── media/                # Directorio para medios generados (e.g., QR codes)
└── manage.py             # Script de gestión de Django
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un "pull request" con tus cambios propuestos. Asegúrate de seguir las convenciones de codificación y de realizar las pruebas adecuadas antes de enviar tu contribución.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

## Contacto

Para cualquier pregunta o sugerencia, puedes contactarme a través de [assizalcaraz@gmail.com](mailto:assizalcaraz@gmail.com).
```
