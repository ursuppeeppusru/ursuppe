# ps_submission/views.py
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timedelta

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission

def today():
    today = timezone.now().date()
    return today

def today_plus_2w():    
    today_plus_2w = today() + timedelta(weeks=2)
    return today_plus_2w

@cache_page(60 * 60)
def highlights(request):
    # Only object which are marked as published
    highlighted_submissions = ExhibitionSubmission.objects.filter(published=True, highlight=True).order_by('-exhibition_end')
    highlighted_event_submissions = CalendarSubmission.objects.filter(published=True, highlight=True).filter(exhibition_end__gte=today()).order_by('exhibition_end')
    all_current_event_submissions = CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).filter(exhibition_opening__lte=today()).order_by('exhibition_end')
    return render(request, 'highlights.html', {'highlighted_submissions': highlighted_submissions, 'highlighted_event_submissions': highlighted_event_submissions, 'all_current_event_submissions': all_current_event_submissions, 'today': today(), 'today_plus_2w': today_plus_2w()})