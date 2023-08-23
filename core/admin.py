from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store3.admin import ProductAdmin
from tags.models import TaggedItem
from . models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
  add_fieldsets=(
     (None, {
        'classes': ('wide',),
        'fields':('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
     }
      ),
  )
    



class TagInline(GenericTabularInline):
    autocomplete_fields= ['tag']
    model=TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines=[TagInline]