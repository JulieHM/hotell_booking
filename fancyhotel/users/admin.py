from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_cleaner', 'is_investor')
    list_filter = ('is_staff', 'is_cleaner', 'is_investor',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Details', {'fields': ('first_name', 'last_name', 'phone_number'),}),
        ('Permissions', {'fields': ('is_cleaner', 'is_investor', 'is_staff', 'is_active'),
                         'classes': ('collapse',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number',)
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)