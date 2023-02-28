from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Dictionary


class DictionaryForm(forms.ModelForm):
    alpha_position = forms.CharField(widget=forms.RadioSelect)

    class Meta:
        model = Dictionary
