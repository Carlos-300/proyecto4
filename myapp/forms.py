from django import forms



class validar_unir_pdf(forms.Form):
    file_unir_pdf = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def _get_name(self):
        return self._name


class validar_dividir_pdf(forms.Form):
    file_dividir_pdf = forms.FileField(widget=forms.ClearableFileInput())
    numero_de_pag_pdf = forms.IntegerField(min_value=1)

    def _get_name(self):
        return self._name


class validad_extraer_pdf(forms.Form):
    file_extraer_pdf = forms.FileField(widget=forms.ClearableFileInput())
    numero_pag = forms.IntegerField(min_value=1)

    def _get_name(self):
        return self._name

    
class validad_extraer_pdf_range(forms.Form):
    file_extraer_pdf_range = forms.FileField(widget=forms.ClearableFileInput())
    numero_pag_inicio = forms.IntegerField(min_value=1)
    numero_pag_final = forms.IntegerField(min_value=1)

    def _get_name(self):
        return self._name
