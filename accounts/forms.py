from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Password"
        })
    )

    role = forms.ChoiceField(
        choices=[
            ("student", "Student"),
            ("teacher", "Teacher"),
            ("admin", "Admin"),
        ],
        widget=forms.HiddenInput()
    )