from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from store.data.user.models import CustomUser
from store.interfaces.forms.user import UserCreationForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = UserCreationForm
    list_display = ('email', 'username', 'is_active',)
    list_filter = ('email', 'username', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password','first_name','last_name','date_of_birth','created')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username','created')


admin.site.register(CustomUser, CustomUserAdmin)