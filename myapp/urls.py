from django.urls import path


from . import views


urlpatterns = [
   
    path('index/', views.vistageneral),
    path('', views.vistageneral),
    path('unir_pdf/',views.form_unir_pdf,name="unir_pdf"),
    path('dividir_pdf/',views.form_dividir_pdf,name="dividir_pdf"),
    path('extraer_pdf/',views.form_extraer_pdf,name="extraer_pdf"),
    path('extraer_pdf_range/',views.extraer_rango_pag,name="extraer_pdf_range"),

   
]
