from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class FormularioCargarViaje(forms.Form):

    opciones = (('Tandil', 'Tandil'), ('CABA', 'CABA'))

    origen = forms.ChoiceField(label='Origen', choices=opciones, required=True)
    destino = forms.ChoiceField(label='Destino', choices=opciones, required=True)
    fecha = forms.DateField(widget=DateInput, required=True)
    observaciones = forms.CharField(label='Observaciones', widget=forms.Textarea(attrs={'rows':4, 'cols':50}))

class FormularioVerViaje(forms.Form):

    opciones = (('Tandil', 'Tandil'), ('CABA', 'CABA'))

    origen = forms.ChoiceField(label='Origen (*) ', choices=opciones, required=True)
    destino = forms.ChoiceField(label='Destino (*) ', choices=opciones, required=True)
    fecha = forms.DateField(widget=DateInput)