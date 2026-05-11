from django.contrib import admin
from .models import Bus, Student, BusEntry


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['name', 'route', 'capacity', 'driver_name', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'route', 'driver_name']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    fieldsets = (
        ('Bus Information', {
            'fields': ('uuid', 'name', 'route', 'capacity')
        }),
        ('Driver Information', {
            'fields': ('driver_name', 'driver_phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'email', 'bus', 'is_active']
    list_filter = ['is_active', 'bus', 'created_at']
    search_fields = ['name', 'roll_number', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'roll_number', 'email', 'phone_number')
        }),
        ('Bus Assignment', {
            'fields': ('bus',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BusEntry)
class BusEntryAdmin(admin.ModelAdmin):
    list_display = ['student', 'bus', 'date', 'entry_time', 'exit_time']
    list_filter = ['date', 'bus', 'created_at']
    search_fields = ['student__name', 'student__roll_number', 'bus__name']
    readonly_fields = ['date', 'created_at', 'duration_in_bus']
    fieldsets = (
        ('Entry Information', {
            'fields': ('student', 'bus', 'entry_time', 'exit_time')
        }),
        ('Additional Info', {
            'fields': ('date', 'duration_in_bus', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return self.readonly_fields + ['entry_time']
        return self.readonly_fields
