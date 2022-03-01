from django.contrib.auth import forms
from django.db.models import fields
from .models import *
from django import forms


class HospitalForm(forms.ModelForm):
    class Meta:
        model=Hospital
        exclude=("userlink","hospital_latitude","hospital_longitude",)

        # def clean_hospital_name(self,*args,**kwargs):
        #     return self.cleaned_data.get('hospital_name').title()

        # def clean_contact(self,*args,**kwargs):
        #     number=len(str(self.cleaned_data.get('contact')))
        #     if number>11 or number<10:
        #         raise forms.ValidationError("Enter a Valid Contact number")
        #     else:
        #         return self.cleaned_Data.get('contact')