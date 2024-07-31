# ps_calendar/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, timedelta
from django.db.models import Q

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
    return timezone.now().date()

def today_plus_2w():    
    return today() + timedelta(weeks=2)

# Current events
@cache_page(60 * 60)
def event_list(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started, as well as opening date for one-day events
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(Q(exhibition_end__gte=today()) | Q(opening__contains=today())).filter(Q(exhibition_opening__lte=today()) | Q(opening__contains=today())).order_by('exhibition_end')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Upcoming events
@cache_page(60 * 60)
def event_list_upcoming(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has NOT started, as well as NOT started for opening date for one-day events
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(Q(exhibition_opening__gte=today()) | Q(opening__gt=today())).order_by('exhibition_opening')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Past events
@cache_page(60 * 60)
def event_list_past(request):
    # Only objects which are marked as published and where end date has exceeded, as well as opening date for one-day events
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(Q(exhibition_end__lt=today()) | Q(opening__lt=today())).order_by('exhibition_end')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Closing soon (2 weeks)
@cache_page(60 * 60)
def event_list_closing_soon(request):
    # Only objects which are marked as published and where end date is between today and in two weeks
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__range=(today(), today_plus_2w())).order_by('exhibition_end')
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})

# Openings this week
@cache_page(60 * 60)
def event_list_openings_this_week(request):
    date = today()
    start_week = date - timedelta(date.weekday())
    end_week = start_week + timedelta(7)

    # Only objects which are marked as published and where opening date is in this week
    event_submissions = CalendarSubmission.objects.filter(published=True).filter(opening__range=(start_week, end_week)).order_by('opening')
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
        'calendar__one_day_event',
        'calendar__exhibition_opening',
        'calendar__exhibition_end',
        'calendar__opening_hours',
        'calendar__opening',
        'calendar__opening_hours_for_opening_date',
        'calendar__description',
        'calendar__slug',
        'image'
        ).filter(calendar__published=True).filter(Q(calendar__exhibition_end__gte=today()) | Q(calendar__opening__gte=today())).order_by('calendar__exhibition_end')
    return JsonResponse({"event_submissions": list(event_submissions)})

# Event detail
@cache_page(60 * 60)
def event_detail(request, event_id, event_project_title):
    event = get_object_or_404(CalendarSubmission, id=event_id)
    return render(request, 'event_detail.html', {'event': event, 'today': today(), 'today_plus_2w': today_plus_2w()})