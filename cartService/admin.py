from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .serializers import CustomUserSerializer
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, UserProfile, Category, Product, Order, Cart
# Register your models here.

@admin.register(CustomUser)# To modify my CustomUSer profile
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser
    
    filter_horizontal = []

    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        'is_admin'
    )

    list_filter = ("is_active", "is_staff", "is_superuser", 'is_admin')
    
    fieldsets = (
        
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", 
                        "is_staff",
                        "is_superuser", 'is_admin', 
                        "groups","user_permissions"
                        )}),
       
        # ("Dates", {"fields": ("last_login", "date_joined")}),
        # ("Important dates", {"fields": ("last_login", "date_joined")}),
        #am using AbstractBaseUser 
        #The AbstractBaseUser class does not include the date_joined, 
        # groups, and user_permissions fields by default. 
        # These fields are provided by the AbstractUser class,
        #  which is a subclass of AbstractBaseUser and 
        # includes additional user-related fields.2079804682
        # ("Groups and permissions", {"fields": ("groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", 
                           "is_active","is_staff","is_superuser"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def display_date_joined(self, obj):
        return obj.date_joined

    display_date_joined.short_description = "Date Joined"

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.unregister(Group)
