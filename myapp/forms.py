from django import forms
from django.core.exceptions import ValidationError
import os
from PyPDF2 import PdfReader,PdfFileReader



class validar_unir_pdf(forms.Form):
    file_unir_pdf = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True }), required=True)

    def _get_name(self):
        return self._name

    def clean_file_unir_pdf(self):
        docs = self.files.getlist('file_unir_pdf')
        contador= 0
        for doc in docs:
            input_pdf = PdfFileReader(doc)
            total_pag = input_pdf._get_num_pages()
            contador= contador + total_pag
        if len(docs)<2:
            raise ValidationError("Tienes que agregar como mínimo 2 Documentos")
        if contador> 1000 :
            raise ValidationError("Tus docs tienen :"+str(contador)+" y el max de pág es 1000")
        return docs

class valirdar_carpeta_pdf(forms.Form):
    file_carpeta = forms.FileField(
        widget=forms.ClearableFileInput())
    RadioOptions=forms.RadioSelect()

    
    def clean_file_carpeta(self):
        docs = self.files.getlist('file_carpeta')
        contador= 0
        for doc in docs:
            input_pdf = PdfFileReader(doc)
            total_pag = input_pdf._get_num_pages()
            contador= contador + total_pag
        print(len(docs))
        if len(docs)<3:
            raise ValidationError("Se solicitan como mínimo 3 documentos dentro de la carpeta")
        if len(docs)>50:
            raise ValidationError("La cantidad maxima de docs por carpeta son 50")
        if contador> 1000 :
            raise ValidationError("Tus docs tienen :"+str(contador)+" y el max de pág es 1000")
        return docs

    def clean_RadioOptions(self):
        radio = self.cleaned_data("RadioOptions")
        if radio == None:
            raise ValidationError("Tienes que ingresar un Orden para el documento")
        return radio
        

class validar_dividir_pdf(forms.Form):
    file_dividir_pdf = forms.FileField(widget=forms.ClearableFileInput(), required=True)
    numero_de_pag_pdf = forms.IntegerField(min_value=1, required=True)

    def clean_file_dividir_pdf(self):
        docs = self.files.__getitem__('file_dividir_pdf')
        input_pdf = PdfFileReader(docs)
        total_pag = input_pdf._get_num_pages()
        if total_pag>1000:
            raise ValidationError("Tu doc tienen :"+str(total_pag)+" y el max de pág es 1000 ")
        return docs

    def clean_numero_de_pag_pdf(self):
        numero = self.cleaned_data["numero_de_pag_pdf"]
        if self.files:
            docs = self.files.__getitem__('file_dividir_pdf')
            input_pdf = PdfFileReader(docs)
            total_pag = input_pdf._get_num_pages()
            if numero>= total_pag:
                raise ValidationError("La cantidad de hojas por Doc sobrepasa el total de "+str(total_pag))
            if numero<=0:
                raise ValidationError("Tienes que ingresar un numero")
        else:
            raise ValidationError("Tienes que ingresar un documento")
        return numero
        

class validad_extraer_pdf(forms.Form):
    file_extraer_pdf = forms.FileField(widget=forms.ClearableFileInput(), required=True)
    numero_pag = forms.IntegerField(min_value=1, required=True)

    def clean_file_extraer_pdf(self):
        docs = self.files.__getitem__('file_extraer_pdf')
        input_pdf = PdfFileReader(docs)
        total_pag = input_pdf._get_num_pages()
        if total_pag>1000:
            raise ValidationError("Tu doc tienen :"+str(total_pag)+" y el max de pág es 1000 ")
        return docs
    

    def clean_numero_pag(self):
        numero = self.cleaned_data['numero_pag']
        if self.files:
            docs = self.files.__getitem__("file_extraer_pdf")
            input_pdf = PdfFileReader(docs)
            total_pag = input_pdf._get_num_pages()
            if numero > total_pag :
                raise ValidationError("el numero no puede ser igual o superior a "+str(total_pag))
            if numero<=0:
                raise ValidationError("Tienes que ingresar algun numero")
        else:
            raise ValidationError("Tienes que ingresar algun documento")
        return numero

class validad_extraer_pdf_range(forms.Form):
    file_extraer_pdf_range = forms.FileField(widget=forms.ClearableFileInput(), required=True)
    numero_pag_inicio = forms.IntegerField(min_value=1, required=True)
    numero_pag_final = forms.IntegerField(min_value=1, required=True)
   
    def clean_file_extraer_pdf_range(self):
        docs = self.files.__getitem__('file_extraer_pdf_range')
        input_pdf = PdfFileReader(docs)
        total_pag = input_pdf._get_num_pages()
        if total_pag>1000:
            raise ValidationError("Tu doc tienen :"+str(total_pag)+" y el max de pág es 1000 ")
        return docs

    def clean_numero_pag_inicio(self):
        numero_inicio = self.cleaned_data["numero_pag_inicio"]
        if self.files:
            docs = self.files.__getitem__('file_extraer_pdf_range')
            input_pdf = PdfFileReader(docs)
            total_pag = input_pdf._get_num_pages()
            if numero_inicio>= total_pag:
                raise ValidationError("El N° inicial NO puede ser igual o superior a "+str(total_pag))
            if numero_inicio<=0:
                raise ValidationError("Tienes que ingresar algun numero")
        else:
            raise ValidationError("Tienes que ingresar algun documento")
        return numero_inicio 

    def clean_numero_pag_final(self):
        numero_final = self.cleaned_data["numero_pag_final"]
        if self.files:
            docs = self.files.__getitem__('file_extraer_pdf_range')
            input_pdf = PdfFileReader(docs)
            total_pag = input_pdf._get_num_pages()
            if numero_final > total_pag:
                raise ValidationError("El N° final NO ser superior a "+str(total_pag))
            if numero_final <=0:
                raise ValidationError("Tienes que ingresar algun numero")
        else:
            raise ValidationError("Tienes que ingresar algun documento")
        return numero_final
    
class validad_cambiar_tamano(forms.Form):
    file_cambiar_tamano = forms.FileField(widget=forms.ClearableFileInput(), required=True)
    inlineRadioOptions = forms.RadioSelect()

    def clean_file_cambiar_tamano(self):
        docs = self.files.__getitem__('file_cambiar_tamano')
        input_pdf = PdfFileReader(docs)
        total_pag = input_pdf._get_num_pages()
        if total_pag>1000:
            raise ValidationError("Tu doc tienen :"+str(total_pag)+" y el max de pág es 1000 ")
        return docs

class validad_Rotar_hoja(forms.Form):
    file_rotar = forms.FileField(widget=forms.ClearableFileInput(), required=True)
    numero_pag_rotate = forms.IntegerField(min_value=1, required=True)
    escaladoxy = forms.FloatField(required=True)
    ejex=forms.IntegerField()
    ejexy=forms.IntegerField()

    def clean_file_rotar(self):
        docs = self.files.__getitem__('file_rotar')
        input_pdf = PdfFileReader(docs)
        total_pag = input_pdf._get_num_pages()
        if total_pag>1000:
            raise ValidationError("Tu doc tienen :"+str(total_pag)+" y el max de pág es 1000 ")
        return docs

class validar_file_mostrar(forms.Form):
    file_mostrar_pdf = forms.FileField(widget=forms.ClearableFileInput(), required=True)

    def clean_file_mostrar_pdf(self):
        docs = self.files.__getitem__('file_mostrar_pdf')
        input_pdf = PdfFileReader(docs)
        total_pag = input_pdf._get_num_pages()
        if total_pag>1000:
            raise ValidationError("Tu doc tienen :"+str(total_pag)+" y el max de pág es 1000 ")
        return docs