from django import forms

from .models import Local


class LocalForm(forms.ModelForm):


    class Meta:
        model = Local
        fields = [
            "tag_name",
            "address",
            "rent_price"
        ]
        widgets = {
            'tag_name': forms.TextInput(
                attrs={'placeholder': 'Étiquette'}
            ),
            'address': forms.TextInput(
                attrs={'placeholder': 'Adresse'}
            ),
            'rent_price': forms.TextInput(
                attrs={'placeholder': 'Prix de location fixé'}
            ),
        }




