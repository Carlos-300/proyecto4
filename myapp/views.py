from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter
from django.shortcuts import render
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from .forms import validar_unir_pdf, validar_dividir_pdf, validad_extraer_pdf, validad_extraer_pdf_range
import tempfile
from django.contrib import messages
import zipfile36 
import os
import pathlib


# Create your views here.}
def vistageneral(request):
    return render(request, 'indexPDF.html')


def form_unir_pdf(request):
    if request.method == 'POST':
       # llamamos a la funcion de agregados de PyPDF
        merger = PdfMerger()
        form = validar_unir_pdf(request.POST, request.FILES)
        # creamos una carpeta temporal
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            # obtenemos los objetos ingresados del input file
            documentos = request.FILES.getlist('file_unir_pdf')
            print(documentos)
            contador = 0
            for x in documentos:
                contador = contador+1
                file_name = x.name
                print(file_name)
            if contador > 1:
                for file in documentos:
                    merger.append(file)
                    # devolvemos el archivo terminado
                merger.write(temp_dir.name + "/Compilado-unir-pdf.pdf")
                # llamamos al archivo y se lo pasamos al response por return para descargar el archico
                pdf_file = open(
                    temp_dir.name + '/Compilado-unir-pdf.pdf', 'rb')
                response = HttpResponse(FileWrapper(
                    pdf_file), content_type='text/pdf')
                response['Contwent-Disposition'] = 'attachment; filename="%s"' % 'Compilado-unir-pdf.pdf'
                # cerramos la funcion
                merger.close()
                return response
            elif contador <= 1: 
                messages.error(request,"debes entregar como minimo 2 documentos")
                return render(request, "indexPDF.html", {"ventana1": True, "form": form})
        else:
            # eliminamos la carpeta con todo
            temp_dir.cleanup()
    return render(request, "indexPDF.html")


def form_dividir_pdf(request):
    if request.method == 'POST':
        form = validar_dividir_pdf(request.POST, request.FILES)
        temp_dir = tempfile.TemporaryDirectory()
        myzip = zipfile36.ZipFile(temp_dir.name + "/documentos.zip","w")
        if form.is_valid():
            # obtenemos los objetos ingresados del input file
            numero_de_pag = request.POST['numero_de_pag_pdf']
            documento = request.FILES.get('file_dividir_pdf')
            input_pdf = PdfFileReader(documento)
            merger = PdfMerger()
            
            divisor = int(numero_de_pag)
            total_pag = input_pdf._get_num_pages()
            star_pag=[]
            end_pag=[]
            for x in range(0,total_pag,divisor):
                star_pag.append(x+1)
            for y in range(divisor,total_pag,divisor):
                end_pag.append(y)
            end_pag.append(total_pag)
            for i,o in zip(star_pag,end_pag):
                output = PdfFileWriter()
                for z in range(i-1,o):
                    output.addPage(input_pdf.getPage(z))
                output.write(temp_dir.name+'/Doc_'+str(i)+'_'+str(o)+'.pdf')
                print(temp_dir.name)
                myzip.write(temp_dir.name+'/Doc_'+str(i)+'_'+str(o)+'.pdf')

            myzip.close()
            


            
            pdf_file = open(temp_dir.name + '/documentos.zip', 'rb')
            response = HttpResponse(FileWrapper(pdf_file), content_type='text/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % "documentos.zip"
            return response
            
                
                    
    return render(request, "indexPDF.html")


def form_extraer_pdf(request):
    if request.method == 'POST':
        # llamamos a la funcion de agregados de PyPDF
        form = validad_extraer_pdf(request.POST, request.FILES)
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            # obtenemos los objetos ingresados del input file
            numero_pag = request.POST['numero_pag']
            documento = request.FILES.get('file_extraer_pdf')
            print(numero_pag, documento)
            pag_pdf = int(numero_pag)-1
            input_pdf = PdfFileReader(documento)
            total_pag = input_pdf._get_num_pages()
            if pag_pdf <= total_pag:
                output = PdfFileWriter()
                output.addPage(input_pdf.getPage(pag_pdf))
                output.write(temp_dir.name + '/extract_page'+str(numero_pag)+'.pdf')
                pdf_file = open(temp_dir.name + '/extract_page'+str(numero_pag)+'.pdf', 'rb')
                response = HttpResponse(FileWrapper(
                    pdf_file), content_type='text/pdf')
                response['Content-Disposition'] = 'attachment; filename="%s"' % '/extract_page'+str(numero_pag)+'.pdf'
                # cerramos la funcion
                return response
            else:

                messages.error(request,
                               "la página no se encuentra, El doc tiene en total " + str(total_pag)+" páginas")
                return render(request, "indexPDF.html", {"ventana5": True, "form": form})
        else:
            # eliminamos la carpeta con todo
            temp_dir.cleanup()
            # temp_archivo.close()
    return render(request, "indexPDF.html")




def extraer_rango_pag(request):
    if request.method == 'POST':
        # llamamos al post con sus datos de entrada
        form = validad_extraer_pdf_range(request.POST, request.FILES)
        # se crea un directorio temporal
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            # separamos los datos del post
            numero_pag_inicio = request.POST['numero_pag_inicio']
            numero_pag_final = request.POST['numero_pag_final']
            documento = request.FILES.get('file_extraer_pdf_range')
            pag_pdf_inicio = int(numero_pag_inicio)-1
            pag_pdf_final = int(numero_pag_final)-1
            # abrimos el pdf y obtenemos la cantida de pag q tiene
            input_pdf = PdfFileReader(documento)
            total_pag = input_pdf._get_num_pages()
            # comparamos los datos y verificamos que no sobrepase el total de pag
            if pag_pdf_inicio < pag_pdf_final:
                if pag_pdf_inicio < total_pag or pag_pdf_final <= total_pag:
                    output = PdfFileWriter()
                    for x in range(pag_pdf_inicio, pag_pdf_final):
                        output.addPage(input_pdf.getPage(x))
                    output.write(temp_dir.name + '/extract_page_rage.pdf')
                    pdf_file = open(
                        temp_dir.name + '/extract_page_rage.pdf', 'rb')
                    response = HttpResponse(FileWrapper(
                        pdf_file), content_type='text/pdf')
                    response['Content-Disposition'] = 'attachment; filename="%s"' % 'extract_page_rage.pdf'
                    # cerramos la funcion
                    return response
                else:
                    messages.error(
                        request, "la páginas no se encuentran, El doc tiene en total " + str(total_pag)+" páginas")
                    temp_dir.cleanup()
                    return render(request, "indexPDF.html", {"ventana6": True, "form": form})
            else:
                messages.error(
                    request, "El rango de las paginas de inicio y final no puede ser el mismo")
                temp_dir.cleanup()
                return render(request, "indexPDF.html", {"ventana6": True, "form": form})
        else:
            temp_dir.cleanup()
    return render(request, "indexPDF.html")
