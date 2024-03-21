# ps_calendar/urls.py
from django.urls import path
from .views import calendar_submission_create, event_list, event_list_past, event_list_upcoming, event_list_closing_soon, event_map, json_event_list, event_detail

urlpatterns = [
    path('create', calendar_submission_create, name='calendar_submission_create'),
    path('', event_list, name='event_list'),
    path('upcoming', event_list_upcoming, name='event_list_upcoming'),
    path('past', event_list_past, name='event_list_past'),
    path('closing-soon', event_list_closing_soon, name='event_list_closing_soon'),
    path('map', event_map, name='event_map'),
    path('json', json_event_list, name='json_event_list'),
    path('<int:event_id>-<slug:event_project_title>/', event_detail, name='event_detail'),
    # Add more patterns as needed
]
