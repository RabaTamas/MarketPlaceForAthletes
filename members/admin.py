from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_items')

    def display_items(self, obj):
        return obj.get_items()

    display_items.short_description = 'Advertisements' 

admin.site.register(Profile, ProfileAdmin)