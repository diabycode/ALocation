from typing import Iterable, Optional
from django.db import models


class HasAlreadyAssignedTenant(Exception):
    pass

class SinceDateAssignedWithoutTenant(Exception):
    pass


class Local(models.Model):
    tag_name = models.CharField(max_length=130)
    current_tenant = models.ForeignKey("renter.Renter", on_delete=models.SET_NULL, null=True, blank=True)
    rent_price = models.FloatField(default=0, blank=True)
    address = models.CharField(max_length=150)
    rented_since = models.DateField(blank=True, null=True)

    added_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locaux'

    def __str__(self):
        return self.tag_name
    
    def save(self, *args, **kwargs) -> None:
        if self.rented_since and not self.current_tenant:
            raise SinceDateAssignedWithoutTenant("Impossible d'ajouter une date de location à un local sans locataire ! ")
        return super().save(*args, **kwargs)





