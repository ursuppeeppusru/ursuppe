# ps_calendar/admin.py
from django.contrib import admin
from .models import CalendarSubmission, CalendarImages, OpeningHours
from .forms import CalendarSubmissionAdminForm, CalendarImagesForm, OpeningHoursForm

# @admin.register(CalendarSubmission)
# class CalendarSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('project_title', 'artists', 'location', 'exhibition_opening', 'exhibition_end', 'consent_to_collect_info')
#     search_fields = ('project_title', 'artists', 'location', 'text_author', 'email')  # Add fields you want to search by
#     list_filter = ('exhibition_opening', 'exhibition_end', 'consent_to_collect_info')  # Add fields you want to filter by


class CalendarImagesInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = CalendarImages
    form = CalendarImagesForm
    extra = 1  # Number of empty forms to display

class CalendarOpeningHoursInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = OpeningHours
    form = OpeningHoursForm
    extra = 1  # Number of empty forms to display

class CalendarSubmissionAdmin(admin.ModelAdmin):
    form = CalendarSubmissionAdminForm
    inlines = [CalendarImagesInline, CalendarOpeningHoursInline]

admin.site.register(CalendarSubmission, CalendarSubmissionAdmin)