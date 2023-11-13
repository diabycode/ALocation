from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib import admin

from .models import Renter, Payment


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
        'object_repr',
        'change_message'
    ]

    list_display_links = None    

    # desable the edit link
    def has_change_permission(self, request, obj=None):
        return False    

@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'locals_rented', 'email', 'phone', 'address', 'added_at')


# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('local', 'renter', 'created_at', 'paid', 'paid_at', 'amount')
