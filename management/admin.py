from django.contrib import admin
from .models import SystemAnnouncement, ActivityLog, AdminProfile

@admin.register(SystemAnnouncement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'expiry_date')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'action_type', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    readonly_fields = ('admin_user', 'action_type', 'details', 'timestamp')

    # Security: Admins shouldn't edit logs
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_temple', 'employee_id')
    search_fields = ('employee_id', 'user__email')