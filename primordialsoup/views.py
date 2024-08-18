# ps_submission/views.py
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timedelta
from django.db.models import Q

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission

def today():
    return timezone.now().date()

def today_plus_2w():    
    return today() + timedelta(weeks=2)

@cache_page(60 * 60)
def highlights(request):
    # Only object which are marked as published
    highlighted_submissions = ExhibitionSubmission.objects.filter(published=True, highlight=True).order_by('-created_at')[:5]
    highlighted_event_submissions = CalendarSubmission.objects.filter(published=True, highlight=True).filter(Q(exhibition_end__gte=today()) | Q(opening__gte=today())).order_by('exhibition_end')
    all_current_event_submissions = CalendarSubmission.objects.filter(published=True).filter(Q(exhibition_end__gte=today()) | Q(opening__contains=today())).filter(Q(exhibition_opening__lte=today()) | Q(opening__contains=today())).order_by('exhibition_end')
    all_upcoming_event_submissions = CalendarSubmission.objects.filter(published=True).filter(Q(opening__gte=today())).order_by('opening')
    return render(request, 'highlights.html', {'highlighted_submissions': highlighted_submissions, 'highlighted_event_submissions': highlighted_event_submissions, 'all_current_event_submissions': all_current_event_submissions, 'all_upcoming_event_submissions': all_upcoming_event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})