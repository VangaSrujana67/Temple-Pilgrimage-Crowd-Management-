from django.contrib import admin
from .models import Temple

@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'state', 'deity', 'created_at')
    list_filter = ('state', 'district')
    search_fields = ('name', 'district', 'deity')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'deity', 'description', 'image')
        }),
        ('Location Details', {
            'fields': ('state', 'district', 'address', 'latitude', 'longitude')
        }),
        ('Temple Layout & Navigation', {
            'fields': ('entry_gate_info', 'exit_gate_info', 'darshan_hall_info')
        }),
    )