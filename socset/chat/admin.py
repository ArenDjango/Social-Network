from django.contrib import admin
from .models import *

class ChatAdmin(admin.ModelAdmin):
    class Meta:
        model = Chat

admin.site.register(Chat)

