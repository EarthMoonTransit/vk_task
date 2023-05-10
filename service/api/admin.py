from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id", "email", "first_name", "last_name", "date_birth", "is_staff")
    list_filter = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "is_staff")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)



admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)