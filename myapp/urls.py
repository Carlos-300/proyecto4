from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path

from . import views


urlpatterns = [
   
    path('index/', views.vistageneral),
    path('', views.vistageneral),
    path('unir_pdf/',views.form_unir_pdf,name="unir_pdf"),
    path('unir_carpeta_pdf/',views.form_carpeta_unir,name="unir_carpeta_pdf"),
    path('dividir_pdf/',views.form_dividir_pdf,name="dividir_pdf"),
    path('extraer_pdf/',views.form_extraer_pdf,name="extraer_pdf"),
    path('extraer_pdf_range/',views.extraer_rango_pag,name="extraer_pdf_range"),
    path('Cambiar_tamano/',views.form_cambiar_tamano,name="Cambiar_tamano"),
    path('Rotar_hoja/',views.form_rotar_pag,name="Rotar_hoja"),
    path('girar/',views.formulario_de_entrega,name="girar"),
    path('salidaDoc/',views.salidaDoc,name="salidaDoc"),
    path('deletepdf/',views.deletepdf,name="deletepdf"),
    path('ejemplo/',views.ver_ejemplo,name="ejemplo"),
    path('montar_hoja/',views.form_montar_documentos,name='montar_hojas'),
    path('montar_salida/',views.montar_salida_doc,name='montar_salida'),
    path('cambiarTamano_salida/',views.cambiar_salida_doc,name='cambiarTamano_salida'),
    

   
]
