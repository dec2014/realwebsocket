from django.contrib import admin

from .models import User
from chat.models import Room,Messages


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Messages)