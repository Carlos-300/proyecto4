from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter,Transformation
from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import tempfile
from django.contrib import messages
import zipfile36
from django.core.exceptions import ValidationError
from reportlab.lib.pagesizes import A4,letter,legal
#letter es carta  A4 es estandar y oficio no esta

from pdf2image import convert_from_path, convert_from_bytes
from .forms import (validar_unir_pdf,
                    validar_dividir_pdf,
                    validad_extraer_pdf,
                    validad_extraer_pdf_range,
                    validad_Rotar_hoja,
                    valirdar_carpeta_pdf,
                    validar_file_mostrar,
                    validar_json,
                    validar_delete,
                    validar_montar_hojas,
                    validar_montar_salida_hojas,
                    validar_cambiar_size)
import os
import base64
import io
from django.conf import global_settings
import json

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

            for file in documentos:
                merger.append(file)

                # devolvemos el archivo terminado
            merger.write(temp_dir.name + "/Compilado-pdf.pdf")
            # llamamos al archivo y se lo pasamos al response por return para descargar el archico
            pdf_file = open(temp_dir.name + '/Compilado-pdf.pdf', 'rb')
            response = HttpResponse(FileWrapper(
                pdf_file), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename=Compilado-pdf.pdf'
            # cerramos la funcion
            merger.close()
            temp_dir.cleanup()
            return response
        else:
            temp_dir.cleanup()
            return render(request, "indexPDF.html", {'ventana1': True, "form": form})
    else:
        return redirect("/index/")


def form_carpeta_unir(request):
    if request.method == 'POST':
       # llamamos a la funcion de agregados de PyPDF
        merger = PdfMerger()
        form = valirdar_carpeta_pdf(request.POST, request.FILES)
        # creamos una carpeta temporal
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            # obtenemos los objetos ingresados del input fileopc
            documentos = request.FILES.getlist('file_carpeta')
            option = request.POST['RadioOptions']
            if option == "option1":
                for x in documentos:
                    merger.append(x)
                merger.write(temp_dir.name + "/Compilado-Carpeta-ASC.pdf")
                merger.close()
                pdf_file = open(
                    temp_dir.name + '/Compilado-Carpeta-ASC.pdf', 'rb')
                response = HttpResponse(FileWrapper(
                    pdf_file), content_type='text/pdf')
                response['Content-Disposition'] = 'attachment; filename=Compilado-Carpeta-ASC.pdf'
                return response
            elif option == "option2":
                for x in reversed(documentos):
                    merger.append(x)
                merger.write(temp_dir.name + "/Compilado-Carpeta-DESC.pdf")
                merger.close()
                pdf_file = open(
                    temp_dir.name + '/Compilado-Carpeta-DESC.pdf', 'rb')
                response = HttpResponse(FileWrapper(
                    pdf_file), content_type='text/pdf')
                response['Content-Disposition'] = 'attachment; filename=Compilado-Carpeta-DESC.pdf'
                temp_dir.cleanup()
                return response
            else:
                temp_dir.cleanup()
                return render(request, "indexPDF.html", {'ventana1': True, 'navCarpeta': True, "form": form})

        else:
            temp_dir.cleanup()
            return render(request, "indexPDF.html", {'ventana1': True, 'navCarpeta': True, "form": form})
    else:
        return redirect("/index/")


def form_dividir_pdf(request):
    if request.method == 'POST':
        form = validar_dividir_pdf(request.POST, request.FILES)
        temp_dir = tempfile.TemporaryDirectory()
        myzip = zipfile36.ZipFile(temp_dir.name+"/documentos.zip", 'a')
        if form.is_valid():
            # obtenemos los objetos ingresados del input file
            numero_de_pag = request.POST['numero_de_pag_pdf']
            documento = request.FILES.get('file_dividir_pdf')

            input_pdf = PdfFileReader(documento)
            divisor = int(numero_de_pag)
            total_pag = input_pdf._get_num_pages()

            star_pag = []
            end_pag = []
            for x in range(0, total_pag, divisor):
                star_pag.append(x+1)
            for y in range(divisor, total_pag, divisor):
                end_pag.append(y)
            end_pag.append(total_pag)

            for i, o in zip(star_pag, end_pag):
                output = PdfFileWriter()
                for z in range(i-1, o):
                    output.addPage(input_pdf.getPage(z))
                output.write(temp_dir.name+'/Doc_' +  str(i)+'_'+str(o)+'.pdf')
                myzip.write(filename=temp_dir.name+'/Doc_'+str(i)+'_' +str(o)+'.pdf', arcname='/Doc_'+str(i)+'_'+str(o)+'.pdf')
            myzip.close()

            pdf_file = open(temp_dir.name + '/documentos.zip', 'rb')
            response = HttpResponse(FileWrapper(pdf_file), content_type='text/zip')
            response['Content-Disposition'] = 'attachment; filename=documentos.zip'
            temp_dir.cleanup()
            return response
        else:
            temp_dir.cleanup()
            return render(request, "indexPDF.html", {'ventana2': True, "form": form})
    else:
        return redirect("/index/")


def form_extraer_pdf(request):
    if request.method == 'POST':
        # llamamos a la funcion de agregados de PyPDF
        form = validad_extraer_pdf(request.POST, request.FILES)
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():

            # obtenemos los objetos ingresados del input file
            numero_pag = request.POST['numero_pag']
            documento = request.FILES.get('file_extraer_pdf')
            pag_pdf = int(numero_pag)-1
            input_pdf = PdfFileReader(documento)

            output = PdfFileWriter()
            output.addPage(input_pdf.getPage(pag_pdf))
            output.write(temp_dir.name + '/extract_page' +
                         str(numero_pag)+'.pdf')

            pdf_file = open(temp_dir.name + '/extract_page' +
                            str(numero_pag)+'.pdf', 'rb')
            response = HttpResponse(FileWrapper(
                pdf_file), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename=extract_page' + \
                str(numero_pag)+'.pdf'
            # cerramos la funcion abrir leer y pasar
            temp_dir.cleanup()
            return response

        else:
            # eliminamos la carpeta con todo
            temp_dir.cleanup()
            return render(request, "indexPDF.html", {'ventana5': True, "form": form})
    else:
        return redirect("/index/")


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
            pag_pdf_final = int(numero_pag_final)
            # abrimos el pdf y obtenemos la cantida de pag q tiene
            input_pdf = PdfFileReader(documento)
            # comparamos los datos y verificamos que no sobrepase el total de pag
            if pag_pdf_inicio < pag_pdf_final:
                output = PdfFileWriter()
                for x in range(pag_pdf_inicio, pag_pdf_final):
                    output.addPage(input_pdf.getPage(x))
                output.write(temp_dir.name + '/extract_pag_' +
                             str((pag_pdf_inicio+1)) + '-'+str(pag_pdf_final) + '.pdf')
                pdf_file = open(temp_dir.name + '/extract_pag_'+str(
                    (pag_pdf_inicio+1)) + '-'+str(pag_pdf_final) + '.pdf', 'rb')
                response = HttpResponse(FileWrapper(pdf_file), content_type='text/pdf')
                response['Content-Disposition'] = 'attachment; filename=extract_pag_' + \
                    str((pag_pdf_inicio+1)) + '-' + \
                    str(pag_pdf_final) + '.pdf'
                # cerramos la funcion
                temp_dir.cleanup()
                return response
            else:
                temp_dir.cleanup()
                form.add_error("numero_pag_final", ValidationError(
                    "El N° inicial no puede superar o ser igual al N°final", "error1"))
                return render(request, "indexPDF.html", {"ventana6": True, "form": form})

        else:
            temp_dir.cleanup()
            return render(request, "indexPDF.html", {"ventana6": True, "form": form})
    else:
        return redirect("/index/")

def pagesize_box(doc):
    documento = PdfFileReader(doc)
    box1 = documento.pages[0].mediabox
    alto = round(box1.height)
    ancho = round(box1.width)
    PostScript = 0.3527777778
    tipo_doc = None
    #legal // oficio
    if ancho == 612 and alto== 1009:
        print("el doc esta en hoja oficio")
        tipo_doc =  "Oficio "+str(216) +" x "+ str(356) + "mm"
        return tipo_doc
    #letter // Carta
    if ancho == 612 and alto == 791 :
        print("El doc esta en hoja carta")
        tipo_doc = "Carta " +str(216) +" x "+ str(279) + "mm"
        return tipo_doc
    #A4
    if ancho == 595 and alto == 842:
        print("el doc esta en hoja A4")
        tipo_doc= "A4 "+str(round(A4[0]*PostScript)) +" x "+ str(round(A4[1]*PostScript)) + "mm"
        return tipo_doc
    else:
        
        ancho2=round(ancho*PostScript)
        alto2= round(alto*PostScript)
        tipo_doc = "El Documento no tiene un formato establecido  "+str(ancho2) +" x "+ str(alto2) + "mm"
        
    return tipo_doc

def form_cambiar_tamano(request):
    if request.method == 'POST':
        # llamamos al post con sus datos de entrada
        form = validad_extraer_pdf_range(request.POST, request.FILES)
        temp_dir1 = tempfile.NamedTemporaryFile(delete=False)
        temp_dir= tempfile.TemporaryDirectory()
        if form.is_valid:
            doc1 = request.FILES.get('file_cambiar_tamano')
            lista_img=[]
            resultado = pagesize_box(doc1)
            print(resultado)
            with open(temp_dir1.name, 'wb+')as destination:
                for chunk in doc1.chunks():
                    destination.write(chunk)
                images = convert_from_path(temp_dir1.name, dpi=50, fmt="PNG",first_page=1 , last_page=1, transparent=True)
                for i in range(len(images)):
                    images[i].save(temp_dir.name+'/paga_abajo_doc1.png')
                    image = open(temp_dir.name+'/paga_abajo_doc1.png', 'rb')
                    image_read = image.read()
                    #image_read = images[i].tobytes()
                    image_64_encode = base64.encodestring(image_read)
                    image_64_decode = image_64_encode.decode()
                    lista_img.append({"imagen": image_64_decode, "id_img": i})

            return render(request, "indexPDF.html", {"ventanaAmostrarCambiarTamano": True, "resultado_size": resultado, "lista_img": lista_img ,"form": form, "ruta_doc1": temp_dir1.name} )
            
    else:
        return redirect("indexPDF.html")


def form_rotar_pag(request):
    if request.method == 'POST':
        # llamamos al post con sus datos de entrada
        form = validad_Rotar_hoja(request.POST, request.FILES)
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid:
            numero_pag_rot = request.POST['numero_pag_rotate']
            escalado = request.POST['escaladoxy']
            ejex = request.POST['ejex']
            ejey = request.POST['ejexy']
            documentos = request.FILES.get('file_rotar')
            input_pdf = PdfFileReader(documentos)
            # creamos un objeto donde guardamos la rotacion
            output2 = PdfFileWriter()
            output2.addBlankPage(width=612.0, height=792.0)
            output2.write(temp_dir.name+"/box.pdf")

            input_pdf2 = PdfFileReader(temp_dir.name+"/box.pdf")
            page_base = input_pdf.pages[int(numero_pag_rot)-1]
            page_box = input_pdf2.pages[0]
            page_base.rotate(90)
            page_box.mergeScaledTranslatedPage(
                page_base, escalado, tx=int(ejex)+0.1, ty=int(ejey)+0.1)

            output = PdfFileWriter()
            output.addPage(page_box)
            output.write(temp_dir.name+"/Rotacion_pag.pdf")

            output3 = PdfFileWriter()

            output3.insert_page(input_pdf2.getPage(0), int(numero_pag_rot)-1)
            output3.write(temp_dir.name+"/hola.pdf")
            # trabajar con % y dividir

            # page_box.mergeScaledTranslatedPage(page_base,0.7,tx=35.9,ty=300.9)
            #page_box.mergeRotatedScaledTranslatedPage(page_base,0,0.7,page_base.mediaBox.getWidth()/2, page_base.mediaBox.getWidth()/2)
            # page_box.mergeRotatedTranslatedPage(page_base,0,tx=0,ty=0,expand= True)#,0.7
            # page_box.scale_to(width=612.0,height=792.0)

            pdf_file = open(temp_dir.name+"/hola.pdf", 'rb')
            response = HttpResponse(FileWrapper(
                pdf_file), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename=hola.pdf'
            return response
    return render("indexPDF.html")


def formulario_de_entrega(request):
    if request.method == 'POST':
        form = validar_file_mostrar(request.POST, request.FILES)
        temp_dir = tempfile.NamedTemporaryFile(delete=False)
        temp_dir2 = tempfile.TemporaryDirectory()
        if form.is_valid():
            documento = request.FILES.get('file_mostrar_pdf')
            # TemporaryUploadedFile archivos grande los guarda en una parte del disco /
            # if(type(documento).__name__ == 'TemporaryUploadedFile'):
            #    file_path = documento.temporary_file_path()
            #    images = convert_from_path(file_path,dpi=30, thread_count=8)
            # InMemoryUploadedFile archivos pequeño los guarda en la memoria    sorttable
            # elif (type(documento).__name__ == 'InMemoryUploadedFile'):
            #    file_read= documento.read()
            #    images= convert_from_bytes(file_read, dpi=30)
            # else:
            
            
            
            with open(temp_dir.name, 'wb+')as destination:
                for chunk in documento.chunks():
                    destination.write(chunk)
                images = convert_from_path(temp_dir.name, dpi=30)

            ver_img = []
            for i in range(len(images)):
                images[i].save(temp_dir2.name+'/page' + str(i) + '.jpg', 'JPEG')
                image = open(temp_dir2.name+'/page' + str(i) + '.jpg', 'rb')
                image_read = image.read()
                image_64_encode = base64.encodestring(image_read)
                image_64_decode = image_64_encode.decode()
                ver_img.append({"imagen": image_64_decode, "id_img": i})

            return render(request, "indexPDF.html", {"ventanaAmostrar": True, "img": ver_img, "form": form, "ruta_doc": temp_dir.name })
        else:
            temp_dir2.cleanup()
            return render(request, "indexPDF.html", {"ventana3": True, "form": form})
    else:
        return redirect("/index/")


def salidaDoc(request):
    if request.method == 'POST':
        form = validar_json(request.POST)
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            ruta_doc = request.POST["ruta_doc"]
            json_ver = request.POST["lista_json"]
            json_ver = json.loads(json_ver)
            if os.path.exists(ruta_doc) == False:
                return render(request, "indexPDF.html",{"venntanaAlerta": True})
            input_pdf = PdfFileReader(ruta_doc)
            output = PdfFileWriter()
            for i in json_ver:
                page = i['numero_pg']
                rotate = i['rotacion_pag']
                if page is None or rotate is None:
                    temp_dir.cleanup()
                    return render(request, "indexPDF.html", {"ventanaAmostrar": True})
                output.addPage(input_pdf.getPage(
                    int(page)).rotate(int(rotate)))
            output.write(temp_dir.name+'/Doc_Orden_rotación.pdf')
            pdf_file = open(temp_dir.name + '/Doc_Orden_rotación.pdf', 'rb')
            response = HttpResponse(FileWrapper(pdf_file), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename=Doc_Orden_rotación.pdf'
            temp_dir.cleanup()
            os.remove(ruta_doc)
            return response
        else:
            temp_dir.cleanup()
            return redirect('/index/')
    return redirect("/index/")

def deletepdf(request):
    if request.method == 'POST':
        form = validar_delete(request.POST)
        ruta_doc = request.POST["ruta_doc"]
        if form.is_valid:
            if os.path.isfile(ruta_doc):
                os.remove(ruta_doc)
            return redirect('/index/')
        return redirect('/index/')
    return redirect('/index/')


#al montar una tienen que ser distintos archivos y mostrar la prira hoja de muerstra 


def form_montar_documentos(request):
    if request.method == 'POST':
        form = validar_montar_hojas(request.POST, request.FILES)
        temp_dir1 = tempfile.NamedTemporaryFile(delete=False)
        temp_dir2 = tempfile.NamedTemporaryFile(delete=False)
        temp_dir= tempfile.TemporaryDirectory()
        if form.is_valid:
            doc1 = request.FILES.get('montar_file')
            doc2 = request.FILES.get('montar_file2')
            lista_img=[]
            lista_img2=[]
            with open(temp_dir1.name, 'wb+')as destination:
                for chunk in doc1.chunks():
                    destination.write(chunk)
                images = convert_from_path(temp_dir1.name, dpi=50, fmt="PNG",first_page=1 , last_page=1, transparent=True)
                for i in range(len(images)):
                    images[i].save(temp_dir.name+'/paga_abajo_doc1.png')
                    image = open(temp_dir.name+'/paga_abajo_doc1.png', 'rb')
                    image_read = image.read()
                    #image_read = images[i].tobytes()
                    image_64_encode = base64.encodestring(image_read)
                    image_64_decode = image_64_encode.decode()
                    lista_img.append({"imagen": image_64_decode, "id_img": i})


            with open(temp_dir2.name, 'wb+')as destination:
                for chunk in doc2.chunks():
                    destination.write(chunk)
                images = convert_from_path(temp_dir2.name, dpi=50, fmt="PNG",first_page=1 , last_page=1, transparent=True)
                for i in range(len(images)):
                    images[i].save(temp_dir.name+'/paga_arriba_doc2.png')
                    image = open(temp_dir.name+'/paga_arriba_doc2.png', 'rb')
                    image_read = image.read()
                    image_64_encode = base64.encodestring(image_read)
                    image_64_decode = image_64_encode.decode()
                    lista_img2.append({"imagen2": image_64_decode, "id_img2": i})
            

            return render(request, "indexPDF.html", {"ventanaAmostrarMontar": True, "lista_img": lista_img, "lista_img2": lista_img2,"form": form, "ruta_doc1": temp_dir1.name , "ruta_doc2": temp_dir2.name})
        else:
            return redirect('/index/')
    else:
        return redirect('/index/')

            
def montar_salida_doc(request):
    if request.method == 'POST':
        form = validar_montar_salida_hojas(request.POST)
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            doc1 = request.POST["ruta_doc1"]
            doc2 = request.POST["ruta_doc2"]
            cifra_y = request.POST["cifra_y"]
            cifra_x = request.POST["cifra_x"]
            input_file1 = PdfFileReader(doc1)
            input_file2 = PdfFileReader(doc2)
            output = PdfFileWriter()
            total_hojas = input_file1._get_num_pages()
            box1 = input_file1.pages[0].mediabox
            cifra_y =float(cifra_y)
            cifra_x =float(cifra_x)
            alto = ((float(box1.height)*cifra_y)/100)
            ancho =((float(box1.width)*cifra_x)/100)
            alto = round(alto,2)    
            ancho = round(ancho,2)
            for x in range(total_hojas):
                lista1 = input_file1.getPage(x)
                lista2 = input_file2.getPage(x)
                lista1.mergeRotatedScaledTranslatedPage(lista2,0,1,tx=ancho,ty=(alto*-1))
                output.addPage(lista1)
            output.write(temp_dir.name+"/pruebas.pdf")
            pdf_file = open(temp_dir.name + '/pruebas.pdf', 'rb')
            response = HttpResponse(FileWrapper(pdf_file), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename=pruebas.pdf'
            temp_dir.cleanup()
            os.remove(doc1)
            os.remove(doc2)
            return response
        else:
            return redirect('/index/')
    else:
        return redirect('/index/')
    

def cambiar_salida_doc(request):
    if request.method == 'POST':
        form = validar_cambiar_size(request.POST)
        temp_dir = tempfile.TemporaryDirectory()
        if form.is_valid():
            doc1 = request.POST["ruta_doc1"]
            dato_alto = request.POST["dato_alto"]
            dato_ancho = request.POST["dato_ancho"]
            PostScript = 0.3527777778
            input_file1 = PdfFileReader(doc1)
            output = PdfFileWriter()
            total_hojas = input_file1._get_num_pages()
            for x in range(total_hojas):
                lista1 = input_file1.getPage(x)
                print(int(dato_ancho),int(dato_alto))
                lista1.scaleTo(width =round(int(dato_ancho)/PostScript),height = round(int(dato_alto)/PostScript))
                output.addPage(lista1)
            output.write(temp_dir.name+"/pruebas.pdf")
            pdf_file = open(temp_dir.name + '/pruebas.pdf', 'rb')
            response = HttpResponse(FileWrapper(pdf_file), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename=pruebas.pdf'
            temp_dir.cleanup()
            os.remove(doc1)
            return response
        else:
            return redirect('/index/')
    else:
        return redirect('/index/')
            
    


def ver_ejemplo(request):
    return render(request, "ejemplo.html")






