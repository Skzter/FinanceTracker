from django import forms
from ToDoApp.models import Ausgaben


class AusgabenForm(forms.ModelForm):
    class Meta:
        model = Ausgaben
        fields = '__all__' 
