from django.contrib.admin.models import LogEntry
from django.contrib import admin


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
        'change_message',
    ]
    
  