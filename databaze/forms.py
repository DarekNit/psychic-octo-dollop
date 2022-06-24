from django import forms
from .models import Klient, Uzivatel, Kontakt, Pojisteni


class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = Uzivatel
        fields = ["email", "password"]


        

class KlientForm(forms.ModelForm):
    pojisteni = forms.ModelMultipleChoiceField(queryset = Pojisteni.objects.all(), required = False)
    class Meta:
        model = Klient
        fields = ["id_klienta", "jmeno", "prijmeni", "narozeni", "pojisteni"]



class KontaktForm(forms.ModelForm):

    class Meta:
        model = Kontakt
        fields = ["email", "kontakt", "adresa"]



class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ["email", "password"]