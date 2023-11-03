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


class LocalFilterForm(forms.Form):

    # hidden filed to activate filters
    filter = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput())

    has_a_tenant = forms.BooleanField(label="occupé", required=False)
    has_no_tenant = forms.BooleanField(label="non occupé", required=False)

    has_a_debt = forms.BooleanField(label="endetté", required=False)
    has_no_debt = forms.BooleanField(label="non endetté", required=False)

    # price range filed to do
