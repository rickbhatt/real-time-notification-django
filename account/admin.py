from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_active", "date_joined")
    readonly_fields = ("id",)
    list_filter = ()
    ordering = ("email",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "last_login",
                    "last_logged_out",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_suspended",
                    "is_payment_defaulter",
                    "is_profile_available",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_suspended",
                    "is_payment_defaulter",
                    "is_profile_available",
                ),
            },
        ),
    )

    search_fields = (
        "id",
        "email",
    )
