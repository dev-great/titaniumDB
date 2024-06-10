from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .forms import *
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {
         'fields': ('phone_number', 'image', 'fcm_token', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ['email', 'first_name', 'last_name', 'phone_number',
                    'is_staff', 'fcm_token',]
    search_fields = ('email', 'first_name', 'last_name', 'phone_number',
                     )
    ordering = ('email', )


admin.site.register(CustomUser, CustomUserAdmin)
