# ps_submission/views.py
from django.shortcuts import render

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission


def highlights(request):
    # Only object which are marked as published
    highlighted_submissions = ExhibitionSubmission.objects.filter(published=True, highlight=True).order_by('-exhibition_end')
    highlighted_event_submissions = CalendarSubmission.objects.filter(published=True)
    return render(request, 'highlights.html', {'highlighted_submissions': highlighted_submissions, 'highlighted_event_submissions': highlighted_event_submissions})