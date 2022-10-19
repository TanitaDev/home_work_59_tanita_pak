from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = "Статус не выбран"
        self.fields['type'].empty_label = "Тип не выбран"

    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 5, 'class': 'input'}),
            'status': forms.Select(attrs={'class': 'input'}),
            'type': forms.Select(attrs={'class': 'input'}),
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти",
                             widget=forms.TextInput(attrs={'class': 'search_input', 'value': ''}))
