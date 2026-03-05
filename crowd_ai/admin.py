from django.contrib import admin
from .models import Festival, PublicHoliday, CrowdOverride

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'impact_level')

@admin.register(PublicHoliday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

@admin.register(CrowdOverride)
class OverrideAdmin(admin.ModelAdmin):
    list_display = ('temple', 'date', 'override_level', 'reason')