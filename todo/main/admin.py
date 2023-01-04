from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import ToDoModels, CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username',
                    'data_joined', 'is_staff',
                    'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'data_joined')
    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()


admin.site.register(ToDoModels)
admin.site.register(CustomUser, CustomUserAdmin)
