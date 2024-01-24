# ps_calendar/urls.py
from django.urls import path
from .views import calendar_submission_create, event_list

urlpatterns = [
    path('submit/', calendar_submission_create, name='calendar_submission_create'),
    path('', event_list, name='event_list'),
    # Add more patterns as needed
]
