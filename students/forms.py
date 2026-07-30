from django import forms
from .models import Student
from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "register_number",
            "name",
            "email",
            "phone",
            "department",
            "year",
            "section",
        ]

        widgets = {
            "register_number": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "year": forms.Select(attrs={"class": "form-select"}),
            "section": forms.TextInput(attrs={"class": "form-control"}),
        }
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["profile_image"]