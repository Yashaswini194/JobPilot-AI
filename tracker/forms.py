from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "company", "role", "job_url", "status", "applied_date",
            "interview_date", "follow_up_date", "job_description", "notes",
        ]
        widgets = {
            "applied_date": forms.DateInput(attrs={"type": "date"}),
            "interview_date": forms.DateInput(attrs={"type": "date"}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "job_description": forms.Textarea(attrs={"rows": 5}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
