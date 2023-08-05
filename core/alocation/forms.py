from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            "autofocus": True,
            "placeholder": "nom d'utilisation"
        }
    ))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "mot de passe"
            }
        ),
    )