from django.contrib import admin
from .models import Items

#register models
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','category','brand','price','type','photo')
    list_editable = ('category','brand','price','type','photo')
    search_fields = ('name','category','brand','type')
    list_filter = ('category','type')
        
admin.site.register(Items, ItemAdmin)