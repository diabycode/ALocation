from typing import Any
from django import forms
from django.db.utils import OperationalError

from renter.models import Renter 
from local.models import Local


try:
    unassigned_locals = (
        (str(local.pk), local.tag_name) for local in Local.objects.all() 
        if not local.is_currently_rented
    )
except OperationalError:
    unassigned_locals = ()


class RenterForm(forms.ModelForm):
    address_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Ligne d’adresse 2'}
        ),
        required=False
    )
    assigned_locals = forms.MultipleChoiceField(
        choices=unassigned_locals,
        required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'multiple-select'}
        )
    )

    class Meta:
        model = Renter
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address"
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Prénom'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Nom'}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': 'Email'}
            ),
            'phone': forms.NumberInput(
                attrs={'placeholder': 'Téléphone'}
            ),
            'address': forms.TextInput(
                attrs={'placeholder': 'Ligne d’adresse 1'}
            ),
        }

    def save(self, commit=True):
        if self.cleaned_data["address_2"]:
            self.cleaned_data["address"] += "\n" + self.cleaned_data["address_2"]
        
        instance: Renter = super().save(commit)

        assigned_locals = self.cleaned_data["assigned_locals"]
        if assigned_locals:
            for local_id in assigned_locals:
                instance.assign_local(
                    local=Local.objects.get(pk=local_id)
                )
        
        instance.save()
        return instance



class RenterFilterForm(forms.Form):

    # hidden filed to activate filters
    filter = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput())

    currently_tenant = forms.BooleanField(label="locataires actuel", required=False)
    not_currently_tenant = forms.BooleanField(label="anciens locataires", required=False)

    has_a_debt = forms.BooleanField(label="endettés", required=False)
    has_no_debt = forms.BooleanField(label="non endettés", required=False)

