from django.contrib import admin
from .models import *

# admin.site.register(CustomUserManager)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'is_active', 'is_staff', 'has_special_access')
    list_filter = ('is_active', 'is_staff', 'has_special_access')
    search_fields = ('phone_number', 'full_name')

    list_select_related = ('profile',)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        profile_data = form.cleaned_data.get('profile')
        if profile_data:
            Profile.objects.update_or_create(user=obj, defaults=profile_data)

admin.site.register(PasswordResetToken)

def approve_registration(modeladmin, request, queryset):
    for pending_registration in queryset:
        user = CustomUser.objects.create_user(phone_number=pending_registration.phone_number, password=pending_registration.password, full_name=pending_registration.full_name)
        pending_registration.delete()
approve_registration.short_description = 'Approve selected registration requests'

def reject_registration(modeladmin, request, queryset):
    queryset.delete()
reject_registration.short_description = 'Reject selected registration requests'

@admin.register(PendingRegistration)
class PendingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at')
    actions = [approve_registration, reject_registration]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'last_name', 'phone_number')