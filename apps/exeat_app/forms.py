from django import forms
from . models import Exeat


class ExeatAPPLYForm(forms.ModelForm):
    class Meta:
        model = Exeat
        fields = ['title','reason','leave_on','return_on']


class UpdateExeatForm(forms.ModelForm):
    class Meta:
        model = Exeat
        fields = "__all__"