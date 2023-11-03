from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    
    error_messages = {
        "invalid_login": (
            "Nom d'utilisateur ou mot de passe incorrect."
        ),
        "inactive": ("Ce compte est inactif."),
    }

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