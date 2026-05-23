
from django import forms


class StatoApprovazione(forms.Form):
    ferie_id = forms.IntegerField()
    stato = forms.IntegerField()


class FerieForm(forms.Form):
    data_selezionata = forms.DateField()
