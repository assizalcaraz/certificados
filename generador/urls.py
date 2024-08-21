from django.urls import path
from . import views

urlpatterns = [
    path('certificado/<uuid:pk>/', views.detalle_certificado, name='detalle_certificado'),
    path('certificado/<uuid:pk>/pdf/', views.exportar_certificado_pdf, name='exportar_certificado_pdf'),
    path('generar/', views.generar_certificado, name='generar_certificado'),
]
