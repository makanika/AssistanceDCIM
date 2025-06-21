from django import forms
from .models import VisitorLog

class VisitorLogForm(forms.ModelForm):
    class Meta:
        model = VisitorLog
        fields = ['visitor_name', 'organization', 'purpose', 'visit_date', 'time_in', 'time_out']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'time_in': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'time_out': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'visitor_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'organization': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'purpose': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
        }
