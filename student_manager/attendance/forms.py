from django import forms
from .models import Subject, AttendanceRecord

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'target_attendance']

class AttendanceRecordForm(forms.ModelForm):
    DELETE_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('D', 'Delete'),
    )

    status = forms.ChoiceField(choices=DELETE_CHOICES)

    class Meta:
        model = AttendanceRecord
        fields = ['status']
