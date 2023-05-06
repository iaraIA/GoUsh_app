from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class FormularioCargarViaje(forms.Form):
    fecha = forms.DateField(widget=DateInput, required=True)
    observaciones = forms.CharField(label='Observaciones', widget=forms.Textarea(attrs={'rows':4, 'cols':50}))
    plazas_disponibles = forms.IntegerField(label='Plazas disponibles', required=True)
    origen_calle = forms.CharField(label='Calle origen', max_length=50, required=True)
    origen_altura = forms.IntegerField(label='Altura origen', required=True)
    destino_calle = forms.CharField(label='Calle destino', max_length=50, required=True)
    destino_altura = forms.IntegerField(label='Altura destino', required=True)

class FormularioVerViaje(forms.Form):
    fecha = forms.DateField(widget=DateInput)
    origen_calle = forms.CharField(label='Calle origen', max_length=50, required=True)
    origen_altura = forms.IntegerField(label='Altura origen', required=True)
    destino_calle = forms.CharField(label='Calle destino', max_length=50, required=True)
    destino_altura = forms.IntegerField(label='Altura destino', required=True)


class FormularioMisViajes(forms.Form):
    origen = forms.CharField(label='Origen', max_length=100, required=False)
    destino = forms.CharField(label='Destino', max_length=100, required=False)
    fecha = forms.DateField(label='Fecha', required=False, widget=forms.SelectDateWidget())
    observaciones = forms.CharField(label='Observaciones', max_length=1000, required=False, widget=forms.Textarea())
