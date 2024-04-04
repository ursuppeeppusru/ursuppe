# ps_calendar/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, timedelta

from .forms import CalendarSubmissionForm, CalendarImagesForm
from .models import CalendarImages, CalendarSubmission


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
            messages.success(request, "Thank you for creating your event. We will look through your submission shortly, and if it meets our criteria it will be published onto this platform. By creating your event you also accept the possibility of being featured on the index page highlighted by our board of artist-moderators, as well as on our social media." )
            return redirect('/events/create')
        else:
            messages.error(request, "Some error occurred. Please re-check your form.")
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

def today_plus_2w():    
    today_plus_2w = today() + timedelta(weeks=2)
    return today_plus_2w

# Current events
@cache_page(60 * 60)
def event_list(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__lte=today()).order_by('exhibition_end')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Upcoming events
@cache_page(60 * 60)
def event_list_upcoming(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has NOT started
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__gte=today()).order_by('exhibition_opening')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Past events
@cache_page(60 * 60)
def event_list_past(request):
    # Only objects which are marked as published and where end date has exceeded
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__lt=today()).order_by('exhibition_end')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Closing soon (2 weeks)
@cache_page(60 * 60)
def event_list_closing_soon(request):
    # Only objects which are marked as published and where end date is between today and in two weeks
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__range=(today(), today_plus_2w())).order_by('exhibition_end')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# map
@cache_page(60 * 60)
def event_map(request):
    return render(request, 'event_submission_map.html')

# Current and upcoming events for map
@cache_page(60 * 60)
def json_event_list(request):
    # JSON
    event_submissions = CalendarImages.objects.values(
        'calendar__id',
        'calendar__project_title',
        'calendar__subtitle',
        'calendar__event_type',
        'calendar__artists',
        'calendar__curators',
        'calendar__location',
        'calendar__link_to_location',
        'calendar__location_address',
        'calendar__latitude',
        'calendar__longitude',
        'calendar__admission',
        'calendar__exhibition_opening',
        'calendar__exhibition_end',
        'calendar__opening_hours',
        'calendar__opening',
        'calendar__opening_hours_for_opening_date',
        'calendar__description',
        'calendar__slug',
        'image'
        ).filter(calendar__published=True).filter(calendar__exhibition_end__gte=today()).order_by('calendar__exhibition_end')
    return JsonResponse({"event_submissions": list(event_submissions)})

@cache_page(60 * 60)
def event_detail(request, event_id, event_project_title):
    event = get_object_or_404(CalendarSubmission, id=event_id)
    return render(request, 'event_detail.html', {'event': event, 'today': today(), 'today_plus_2w': today_plus_2w()})