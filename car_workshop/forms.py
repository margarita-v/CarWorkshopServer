from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    mark = forms.ModelChoiceField(queryset=Mark.objects.all(), label='Mark')
    model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label='Model')
    vin = forms.CharField(min_length=17, max_length=17)
    number = forms.CharField(max_length=8)
    date = forms.DateTimeField()
    status = forms.BooleanField(required=False)
    jobs = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), label='Jobs')

    class Meta:
        model = Task
        fields = ('mark', 'model', 'vin', 'number', 'date', 'status', )
