from django.contrib import admin
from .models import Item, Sport, ItemCondition

# Register your models here.
admin.site.register(ItemCondition)
admin.site.register(Sport)
admin.site.register(Item)
