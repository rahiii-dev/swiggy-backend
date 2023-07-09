from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("userid", "is_staff", "is_active", "user_type")
    list_filter = ("user_type", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("userid", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "userid", "password1", "password2", "user_type", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("userid",)
    ordering = ("userid",)

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)