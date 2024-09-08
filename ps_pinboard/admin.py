# ps_calendar/admin.py
from django.contrib import admin
from .models import Pinboard, PinboardImages
from .forms import PinboardAdminForm, PinboardImagesForm

class PinboardImagesInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = PinboardImages
    form = PinboardImagesForm
    extra = 1  # Number of empty forms to display

class PinboardAdmin(admin.ModelAdmin):
    form = PinboardAdminForm
    list_display = ["title", "category", "created_at", "published"]
    inlines = [PinboardImagesInline]
    # list_filter = ["created_at", "expiration_date"]
    search_fields = ["title"]


admin.site.register(Pinboard, PinboardAdmin)
