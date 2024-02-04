# ps_submission/views.py
from django.shortcuts import render
from django.utils import timezone

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission

def today():
    today = timezone.now().date()
    return today

def highlights(request):
    # Only object which are marked as published
    highlighted_submissions = ExhibitionSubmission.objects.filter(published=True, highlight=True).order_by('-exhibition_end')
    highlighted_event_submissions = CalendarSubmission.objects.filter(published=True, highlight=True).filter(exhibition_end__gte=today()).order_by('exhibition_opening')
    return render(request, 'highlights.html', {'highlighted_submissions': highlighted_submissions, 'highlighted_event_submissions': highlighted_event_submissions})