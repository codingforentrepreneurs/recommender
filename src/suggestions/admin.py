from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Suggestion 

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'object_id', 'user', 'value']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    readonly_fields = ['content_object', 'timestamp']

admin.site.register(Suggestion, SuggestionAdmin)