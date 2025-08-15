from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient model
    """
    list_display = ('name', 'email', 'phone', 'gender', 'created_by', 'created_at')
    list_filter = ('gender', 'created_at', 'created_by')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('address',)
        }),
        ('Medical Information', {
            'fields': ('medical_history',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Doctor model
    """
    list_display = ('name', 'email', 'specialization', 'years_of_experience', 'consultation_fee')
    list_filter = ('specialization', 'created_at')
    search_fields = ('name', 'email', 'specialization', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'license_number', 'years_of_experience')
        }),
        ('Consultation Information', {
            'fields': ('consultation_fee', 'available_from', 'available_to')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """
    Admin configuration for PatientDoctorMapping model
    """
    list_display = ('patient', 'doctor', 'assigned_at', 'is_active')
    list_filter = ('is_active', 'assigned_at', 'doctor__specialization')
    search_fields = ('patient__name', 'doctor__name')
    readonly_fields = ('assigned_at',)
    fieldsets = (
        ('Mapping Information', {
            'fields': ('patient', 'doctor', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('notes', 'assigned_at')
        })
    )