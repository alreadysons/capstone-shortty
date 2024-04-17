from django.contrib import admin
from .models import Message
# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'message', 'timestamp')
    search_fields = ['username', 'message']

admin.site.register(Message, MessageAdmin)