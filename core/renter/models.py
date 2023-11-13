import datetime

from django.db import models

from local.models import Local
from local.models import HasAlreadyAssignedTenant


class PaymentGenerationError(Exception):
    pass


class Payment(models.Model):
    renter = models.ForeignKey("Renter", on_delete=models.CASCADE)
    local = models.ForeignKey("local.Local", on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    paid_at = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return self.renter.fullname
    
    @property
    def due_date(self):
        return self.created_at + datetime.timedelta(days=30)
    
    @property
    def amount(self):
        return self.local.rent_price
    
    @property
    def created_at_str(self):
        return self.created_at.strftime("%d/%m/%Y")


class Renter(models.Model):
    first_name = models.CharField(max_length=130, verbose_name='Prénom')
    last_name = models.CharField(max_length=13, verbose_name='Nom')
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=130, unique=True, blank=False, null=True, verbose_name='Téléphone')
    address = models.CharField(max_length=130, blank=False, null=True, verbose_name='Adresse')

    added_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Ajouté le')
    # payment_date = models.DateField(null=True)

    class Meta:
        verbose_name = 'Locataire'
        verbose_name_plural = 'Locataires'
        ordering = ["-added_at"]

    def __str__(self):
        return self.fullname
    
    @property
    def fullname(self):
        return self.last_name  + ' ' + self.first_name
    
    def generate_payment(self, local: Local) -> Payment:
        if local not in self.local_set.all():
            raise PaymentGenerationError(f"Le local '{local.tag_name}' n'est assigné au locataire '{self.fullname}'")
        
        payment = Payment(renter=self, local=local)
        payment.save()
        return payment
    
    def assign_local(self, local: Local):
        if not local.pk:
            raise local.DoesNotExist
        
        if local.is_currently_rented:
            raise HasAlreadyAssignedTenant("Un locataire est déjà assigné à ce local !")
        
        # local assignment
        self.local_set.add(local)
        local.rented_since = datetime.date.today()
        local.save()
        print(f"Local '{local.tag_name}' assigné au locataire '{self.fullname}'.")

        # Generate payment
        self.generate_payment(local=local)

    def get_all_locals(self):
        return self.local_set.all()
    
    def unpaid_payment_count(self):
        return self.payment_set.filter(paid=False).count()
    
    @property
    def current_payment(self):
        self.payment_set.last()

    @property
    def locals_rented(self):
        return ", ".join([l.tag_name for l in self.local_set.all()])

    @property
    def is_currently_tenant(self):
        return bool(self.local_set.all())



    