Certificados
Este proyecto es una aplicación web para generar y exportar certificados de participación en formato PDF. La aplicación está construida usando Django y utiliza WeasyPrint para generar los PDFs.

Características
Generación de certificados: Los usuarios pueden ingresar los detalles del certificado, que luego son procesados para generar un PDF.
Códigos QR: Cada certificado incluye un código QR único que representa un token generado a partir de los detalles del certificado.
Firmas digitales: El proyecto genera una firma digital para cada certificado utilizando claves RSA.
Exportación a PDF: Los certificados pueden ser exportados y descargados en formato PDF.
Requisitos
Python 3.9 o superior
Docker (opcional, pero recomendado para simplificar el entorno de desarrollo)
Docker Compose (para orquestar los contenedores)
Instalación y configuración
Opción 1: Instalación usando Docker (Recomendada)
Esta opción permite configurar y ejecutar el proyecto fácilmente en un entorno aislado.

Clona el repositorio:

bash
Copiar código
git clone https://github.com/assizalcaraz/certificados
cd certificados
Construye la imagen Docker:

bash
Copiar código
docker-compose build
Inicia la aplicación:

bash
Copiar código
docker-compose up
La aplicación estará disponible en http://localhost:8000.

Montaje de volúmenes:

El docker-compose.yml está configurado para montar volúmenes locales, lo que significa que los cambios que realices en los archivos de la carpeta static o media se reflejarán automáticamente en el contenedor.

yaml
Copiar código
volumes:
  - ./generador/staticfiles/css:/app/generador/staticfiles/css
  - ./media:/app/media
Esto facilita el desarrollo, ya que no es necesario reconstruir la imagen de Docker para cada cambio.

Opción 2: Instalación manual
Si prefieres configurar el proyecto manualmente sin Docker, sigue estos pasos:

Clona el repositorio:

bash
Copiar código
git clone https://github.com/tu_usuario/certificados.git
cd certificados
Crea y activa un entorno virtual:

bash
Copiar código
python3 -m venv env
source env/bin/activate
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Realiza las migraciones y ejecuta el servidor de desarrollo:

bash
Copiar código
python manage.py migrate
python manage.py runserver
La aplicación estará disponible en http://localhost:8000.

Uso
Generar un certificado:

Accede a http://localhost:8000/certificados/generar/ para generar un nuevo certificado.
Ver y exportar certificados:

Después de generar un certificado, podrás visualizarlo y tendrás la opción de exportarlo como un archivo PDF.
Contribución
Si deseas contribuir al proyecto, por favor, sigue estos pasos:

Clona el repositorio.
Crea una rama con una descripción del cambio.
Realiza los cambios y confirma tus commits.
Envía una pull request.
Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

Contacto
Para cualquier pregunta o comentario, puedes contactarme a través de assizalcaraz@gmail.com.