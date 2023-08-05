from django.contrib import admin
from django.db.models import F

from .models import Renter, Payment


@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'locals_rented', 'email', 'phone', 'address', 'added_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('local', 'renter', 'created_at', 'paid', 'paid_at', 'amount')
