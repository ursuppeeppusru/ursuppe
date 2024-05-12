# ps_calendar/admin.py
from django.contrib import admin
from .models import PinBoard
from .forms import PinboardAdminForm


class PinBoardAdmin(admin.ModelAdmin):
    form = PinboardAdminForm
    list_display = ["title", "category", "created_at", "published"]
    # list_filter = ["created_at", "expiration_date"]
    search_fields = ["title"]


admin.site.register(PinBoard, PinBoardAdmin)
