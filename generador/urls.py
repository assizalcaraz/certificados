from django.urls import path
from . import views

urlpatterns = [
    path('generar/', views.generar_certificado, name='generar_certificado'),
    path('<uuid:pk>/', views.detalle_certificado, name='detalle_certificado'),
]
