from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountAdmin(UserAdmin):
    # Fields to be displayed in the admin list view
    list_display = (
        "first_name",
        "last_name",
        "username",
        "email",
        "last_login",
        "date_joined",
        "is_active",
    )
    # Fields that are clickable in the admin list view
    list_display_links = (
        "email",
        "first_name",
        "last_name",
    )
    # Fields that are read-only
    readonly_fields = (
        "last_login",
        "date_joined",
    )
    # Defining the default order in the admin list view
    ordering = ("-date_joined",)

    # Adds a horizantal filter widgets
    filter_horizontal = ()
    # Adds a filter sidebar options
    list_filter = ()
    # Organize forms fields into sections, It will automatically override the default django behaviour
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "username", "phone_number")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_admin", "is_superadmin")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


# Register your models here.
admin.site.register(Account, AccountAdmin)
