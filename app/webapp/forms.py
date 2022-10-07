from django import forms
from .models import *


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=200, label="Заголовок",
                              widget=forms.TextInput(attrs={'class': 'input', 'value': ''}))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5, 'class': 'input'}),
                                  label="Описание")
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Статус", empty_label='Статус не выбран',
                                    widget=forms.Select(attrs={'class': 'input'}))
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Тип", empty_label='Тип не выбран',
                                  widget=forms.Select(attrs={'class': 'input'}))
