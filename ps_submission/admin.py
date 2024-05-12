# ps_submission/admin.py
from django.contrib import admin
from .models import ExhibitionSubmission, ExhibitionImages
from .forms import ExhibitionSubmissionAdminForm, ExhibitionImagesForm

# @admin.register(ExhibitionSubmission)
# class ExhibitionSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('project_title', 'artists', 'location', 'exhibition_opening', 'exhibition_end', 'consent_to_collect_info')
#     search_fields = ('project_title', 'artists', 'location', 'text_author', 'email')  # Add fields you want to search by
#     list_filter = ('exhibition_opening', 'exhibition_end', 'consent_to_collect_info')  # Add fields you want to filter by


class ExhibitionImagesInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = ExhibitionImages
    form = ExhibitionImagesForm
    extra = 5  # Number of empty forms to display

class ExhibitionSubmissionAdmin(admin.ModelAdmin):
    form = ExhibitionSubmissionAdminForm
    inlines = [ExhibitionImagesInline]
    list_display = ["project_title", "published", "highlight"]


admin.site.register(ExhibitionSubmission, ExhibitionSubmissionAdmin)