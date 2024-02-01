# ps_calendar/urls.py
from django.urls import path
from .views import calendar_submission_create, event_list, event_list_json

urlpatterns = [
    path('submit/', calendar_submission_create, name='calendar_submission_create'),
    path('', event_list, name='event_list'),
    path('json', event_list_json, name='event_list_json'),
    # Add more patterns as needed
]
