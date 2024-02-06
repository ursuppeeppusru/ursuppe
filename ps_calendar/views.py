# ps_calendar/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .forms import CalendarSubmissionForm, CalendarImagesForm
from .models import CalendarImages
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from .models import CalendarSubmission


def calendar_submission_create(request):
    ImageFormSet = modelformset_factory(CalendarImages, form=CalendarImagesForm, extra=1)

    if request.method == 'POST':
        submission_form = CalendarSubmissionForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=CalendarImages.objects.none())

        if submission_form.is_valid() and formset.is_valid():
            submission = submission_form.save()
            for form in formset:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.calendar = submission
                    image.save()

            # Add more logic here if needed, such as redirecting to a success page.
            messages.success(request, "Thank you for submitting your event to ursuppe. We will look through your submission shortly, and if it meets our criteria it will be published onto this platform. By submitting your event you also accept the possibility of being featured on the index page highlighted by our board of artist-moderators, as well as on our social media." )
            return redirect('/events')
        else:
            messages.error(request, "Some error occurred while submitting. Please re-check your form.")
    else:
        submission_form = CalendarSubmissionForm()
        formset = ImageFormSet(queryset=CalendarImages.objects.none())

    return render(request, 'calendar_submission_form.html', {
        'submission_form': submission_form,
        'formset': formset,
    })

def today():
    today = timezone.now().date()
    return today

# Current events
def event_list(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__lte=today())
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions})

# Upcoming events
def event_list_upcoming(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has NOT started
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__gte=today())
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions})

# Past events
def event_list_past(request):
    # Only objects which are marked as published and where end date has exceeded
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__lte=today())
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions})

def json_event_list(request):
    # JSON
    # fields = ['slug', 'latitude', 'longitude']
    event_submissions_json = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__lte=today()).values()
    return JsonResponse({"event_submissions_json": list(event_submissions_json)})

def json_event_list_upcoming(request):
    # JSON
    # fields = ['slug', 'latitude', 'longitude']
    event_submissions_json = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__gte=today()).values()
    return JsonResponse({"event_submissions_json": list(event_submissions_json)})

def json_event_list_past(request):
    # JSON
    # fields = ['slug', 'latitude', 'longitude']
    event_submissions_json = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__lte=today()).values()
    return JsonResponse({"event_submissions_json": list(event_submissions_json)})

def event_detail(request, event_id, event_project_title):
    event = get_object_or_404(CalendarSubmission, id=event_id)
    return render(request, 'event_detail.html', {'event': event})